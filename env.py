# ============================================================================
# env.py - Игровая среда для дуэли магов
# ============================================================================
# Это основной файл с логикой игры:
# - Классы магов и спеллов
# - Боевая механика
# - Система состояний и наград для RL
# ============================================================================

class Spell:
    """Описание заклинания"""
    def __init__(self, name, damage=0, heal=0, mana_cost=0, description=""):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.mana_cost = mana_cost
        self.description = description


# Определяем доступные спеллы
SPELLS = {
    0: Spell("Fireball", damage=10, mana_cost=15, description="Базовая атака огнем"),
    1: Spell("Big Spell", damage=20, mana_cost=30, description="Мощная атака"),
    2: Spell("Heal", heal=15, mana_cost=20, description="Исцеление"),
    3: Spell("Shield", mana_cost=10, description="Щит (поглощает урон на 1 ход)"),
    4: Spell("Recharge Mana", mana_cost=0, description="Восстановить ману")
}

NUM_ACTIONS = len(SPELLS)  # 5 возможных действий


class Mage:
    """Класс мага - игрок с HP, mana, shield"""
    
    def __init__(self, name="Маг", max_hp=100, max_mana=100):
        self.name = name
        self.max_hp = max_hp
        self.max_mana = max_mana
        
        self.hp = max_hp
        self.mana = max_mana
        self.shield = False  # есть ли активный щит
        self.last_action = None
    
    def reset(self):
        """Сбросить мага на начальные значения"""
        self.hp = self.max_hp
        self.mana = self.max_mana
        self.shield = False
    
    def take_damage(self, damage):
        """Получить урон, учитывая щит"""
        if self.shield:
            # Щит поглощает четверть урона
            actual_damage = damage // 2
            self.shield = False  # Щит рассеялся
        else:
            actual_damage = damage
        
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Восстановить HP"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def restore_mana(self, amount):
        """Восстановить ману"""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def can_cast_spell(self, action):
        """Проверить, можно ли кастовать спелл (хватает ли маны)"""
        spell = SPELLS[action]
        return self.mana >= spell.mana_cost
    
    def is_alive(self):
        """Проверить, живой ли маг"""
        return self.hp > 0


class MageBattle:
    """Игровая среда - один бой между агентом и ботом"""
    
    def __init__(self):
        self.agent = Mage(name="Агент")    # Наш RL-агент
        self.enemy = Mage(name="Враг")     # Противник с AI
        
        self.turn = 0
        self.max_turns = 100
        self.battle_log = []
        
        self.agent_total_damage = 0
        self.enemy_total_damage = 0
    
    def reset(self):
        """Начать новый бой"""
        self.agent = Mage(name="Агент")
        self.enemy = Mage(name="Враг")
        self.turn = 0
        self.battle_log = []
        self.agent_total_damage = 0
        self.enemy_total_damage = 0
        return self._get_state()
    
    def _get_state(self):
        """Вернуть текущее состояние (дискретизированное)"""
        # Мы дискретизируем состояние в категории, потому что:
        # 1. Q-learning работает лучше с дискретными состояниями
        # 2. 100 значений HP -> бесконечная Q-table, 3-4 категории -> управляемая таблица
        # 3. Агент лучше обобщает: "низкое HP" одно для 5, 10, 15 HP
        
        my_hp = self._discretize_hp(self.agent.hp)
        my_mana = self._discretize_mana(self.agent.mana)
        enemy_hp = self._discretize_hp(self.enemy.hp)
        enemy_mana = self._discretize_mana(self.enemy.mana)
        my_shield = 1 if self.agent.shield else 0
        enemy_shield = 1 if self.enemy.shield else 0
        
        state = (my_hp, my_mana, enemy_hp, enemy_mana, my_shield, enemy_shield)
        return state
    
    def _discretize_hp(self, hp):
        """Превратить HP в категорию: low / medium / high"""
        # 0-33% = low, 34-66% = medium, 67-100% = high
        hp_percent = hp / 100.0
        if hp_percent < 0.34:
            return 0  # low
        elif hp_percent < 0.67:
            return 1  # medium
        else:
            return 2  # high
    
    def _discretize_mana(self, mana):
        """Превратить ману в категорию: low / medium / high"""
        mana_percent = mana / 100.0
        if mana_percent < 0.34:
            return 0  # low
        elif mana_percent < 0.67:
            return 1  # medium
        else:
            return 2  # high
    
    def _enemy_action(self):
        """Логика поведения врага (rule-based)"""
        enemy = self.enemy
        agent = self.agent
        
        # Если враг мертв - не может действовать
        if not enemy.is_alive():
            return None
        
        # 1. Если HP критический и хватает маны - исцеляемся
        if enemy.hp < 30 and enemy.can_cast_spell(2):  # 2 = Heal
            return 2
        
        # 2. Если мана низкая - восстанавливаем
        if enemy.mana < 25 and enemy.can_cast_spell(4):  # 4 = Recharge Mana
            return 4
        
        # 3. Если у врага мало HP и у нас есть мощный спелл - наносим мощный удар
        if agent.hp < 35 and enemy.can_cast_spell(1):  # 1 = Big Spell
            return 1
        
        # 4. Иногда используем щит (если мана средняя и HP низкий)
        if enemy.hp < 50 and enemy.mana > 40 and enemy.can_cast_spell(3) and not enemy.shield:
            if self.turn % 3 == 0:  # Каждый третий ход
                return 3
        
        # 5. В остальных случаях используем базовую атаку
        if enemy.can_cast_spell(0):  # 0 = Fireball
            return 0
        
        # Если не можем кейтовать - восстанавливаем ману
        return 4
    
    def _apply_spell(self, mage, target, action):
        """Применить спелл от mage к target"""
        spell = SPELLS[action]
        
        # Проверяем, хватает ли маны
        if mage.mana < spell.mana_cost:
            return False, "Не хватает маны"
        
        # Тратим ману
        mage.mana -= spell.mana_cost
        mage.last_action = spell.name
        
        # Применяем эффекты
        if spell.damage > 0:
            actual_damage = target.take_damage(spell.damage)
            
            # Если урон был поглощен щитом, возвращаем половину
            if target.shield:
                return True, f"{spell.name} попал! {target.name} потерял {actual_damage} HP (щит поглотил урон!)"
            else:
                return True, f"{spell.name} попал! {target.name} потерял {actual_damage} HP"
        
        if spell.heal > 0:
            mage.heal(spell.heal)
            return True, f"{spell.name} активирован! {mage.name} восстановил {spell.heal} HP"
        
        if spell.name == "Shield":
            mage.shield = True
            return True, f"{spell.name} активирован! {mage.name} получит щит на следующий урон"
        
        if spell.name == "Recharge Mana":
            mage.restore_mana(30)
            return True, f"{spell.name} активирован! {mage.name} восстановил 30 маны"
        
        return True, ""
    
    def step(self, action):
        """
        Один ход боя
        action: 0-4 (индекс спелла для агента)
        Вернуть: (state, reward, done, info)
        """
        self.turn += 1
        
        # Проверяем, не закончился ли бой
        if not self.agent.is_alive() or not self.enemy.is_alive() or self.turn > self.max_turns:
            done = True
            if self.agent.is_alive() and not self.enemy.is_alive():
                reward = 30  # Агент победил
            elif not self.agent.is_alive() and self.enemy.is_alive():
                reward = -30  # Агент проиграл
            else:
                reward = -5  # Ничья за много ходов
            return self._get_state(), reward, done, {}
        
        reward = 0
        done = False
        
        # ===== ХОД АГЕНТА =====
        if not self.agent.can_cast_spell(action):
            # Штраф за попытку кейтовать без маны
            reward -= 5
            action = 4  # Переходим на Recharge Mana
        else:
            # Немного награды за любое валидное действие
            reward += 1
        
        success, msg = self._apply_spell(self.agent, self.enemy, action)
        self.battle_log.append(f"[Агент] {msg}")
        
        if self.agent.last_action in ["Fireball", "Big Spell"]:
            damage_dealt = SPELLS[action].damage
            if self.enemy.shield:
                damage_dealt = damage_dealt // 2
            reward += damage_dealt * 0.1  # +% награды за каждый наносимый урон
            self.agent_total_damage += damage_dealt
        
        # Проверяем победу после хода агента
        if not self.enemy.is_alive():
            done = True
            reward += 30  # Бонус победы
            return self._get_state(), reward, done, {}
        
        # ===== ХОД ВРАГА =====
        enemy_action = self._enemy_action()
        success, msg = self._apply_spell(self.enemy, self.agent, enemy_action)
        self.battle_log.append(f"[Враг] {msg}")
        
        if self.enemy.last_action in ["Fireball", "Big Spell"]:
            damage_dealt = SPELLS[enemy_action].damage
            if self.agent.shield:
                damage_dealt = damage_dealt // 2
            reward -= damage_dealt * 0.1  # -% награды за полученный урон
            self.enemy_total_damage += damage_dealt
        
        # Проверяем поражение после хода врага
        if not self.agent.is_alive():
            done = True
            reward -= 30  # Штраф за поражение
            return self._get_state(), reward, done, {}
        
        # Штраф за слишком長ний бой
        reward -= 0.1
        
        return self._get_state(), reward, done, {}
    
    def render(self):
        """Вывести лог боя и финальное состояние (для demo)"""
        print("\n" + "="*60)
        print("БОЙ ЗАВЕРШЕН")
        print("="*60)
        for log in self.battle_log:
            print(log)
        print("-"*60)
        print(f"Агент: HP={self.agent.hp}/{self.agent.max_hp}, Mana={self.agent.mana}/{self.agent.max_mana}")
        print(f"Враг:  HP={self.enemy.hp}/{self.enemy.max_hp}, Mana={self.enemy.mana}/{self.enemy.max_mana}")
        print(f"Ходов сыграно: {self.turn}")
        print("="*60)
        
        if self.agent.is_alive() and not self.enemy.is_alive():
            print("✓ АГЕНТ ПОБЕДИЛ!")
        elif not self.agent.is_alive() and self.enemy.is_alive():
            print("✗ АГЕНТ ПРОИГРАЛ")
        else:
            print("~ НИЧЬЯ")
        print("="*60 + "\n")
