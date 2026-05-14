# ============================================================================
# visual_demo.py - Красивая визуальная демонстрация боев с Tkinter
# ============================================================================
import tkinter as tk
from tkinter import Canvas
import time
from env import MageBattle, SPELLS
from train import load_agent


class MageBattleVisualizer:
    """Красивая визуализация боя магов с Tkinter"""
    
    def __init__(self, width=1200, height=700):
        self.root = tk.Tk()
        self.root.title("⚔️ Битва магов - Visualization")
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg='#0a0e27')
        self.width = width
        self.height = height
        
        # Canvas для рисования (основной)
        self.canvas = Canvas(self.root, bg='#0a0e27', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Цвета
        self.BG = '#0a0e27'
        self.WHITE = '#FFFFFF'
        self.RED = '#FF3333'
        self.GREEN = '#00FF00'
        self.BLUE = '#00CCFF'
        self.YELLOW = '#FFFF00'
        self.ORANGE = '#FF9900'
        self.PURPLE = '#FF00FF'
        self.DARK_PURPLE = '#660066'
        self.GRAY = '#333333'
        
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Закрытие окна"""
        self.running = False
        self.root.destroy()
    
    def draw_gradient_bar(self, x, y, width, height, value, max_value, color, label):
        """Красивая полоска с градиентом и тенями"""
        # Тень полоски
        self.canvas.create_rectangle(x + 2, y + 2, x + width + 2, y + height + 2, 
                                    fill='#000000', outline='', width=0)
        
        # Фон полоски (ёмкость)
        self.canvas.create_rectangle(x, y, x + width, y + height, fill='#1a1a2e', 
                                    outline='#333333', width=2)
        
        # Полоска значения с градиентом
        if max_value > 0:
            fill_width = (value / max_value) * width
            # Основная полоска
            self.canvas.create_rectangle(x + 1, y + 1, x + fill_width, y + height - 1, 
                                        fill=color, outline='')
            
            # Яркий верхний край (блик)
            self.canvas.create_line(x + 1, y + 1, x + fill_width, y + 1, 
                                   fill=self.WHITE, width=1)
            
            # Темный нижний край
            self.canvas.create_line(x + 1, y + height - 1, x + fill_width, y + height - 1, 
                                   fill='#000000', width=1)
        
        # Текст с значениями
        text = f"{label}: {int(value)}/{int(max_value)}"
        self.canvas.create_text(x + width/2, y + height/2, text=text, 
                               fill=self.WHITE, font=("Courier", 9, "bold"))
    
    def draw_mage(self, x, y, name, hp, max_hp, mana, max_mana, is_agent=True, has_shield=False):
        """Нарисовать красивого мага с тенями и эффектами"""
        color = self.BLUE if is_agent else self.RED
        light_color = '#00FFFF' if is_agent else '#FF6666'
        
        # Тень под магом
        self.canvas.create_oval(x - 80, y + 60, x + 80, y + 75, fill='#444444', outline='')
        
        # Большой кружок для магических сил (аура)
        self.canvas.create_oval(x - 75, y - 75, x + 75, y + 75, 
                               fill='#1a0a2e', outline=light_color, width=3)
        
        # Внутренний круг (кожа)
        self.canvas.create_oval(x - 55, y - 55, x + 55, y + 55, 
                               fill=color, outline=self.WHITE, width=3)
        
        # Внутреннее свечение
        self.canvas.create_oval(x - 52, y - 52, x + 52, y + 52, 
                               fill='', outline=light_color, width=1)
        
        # Шапка/Волосы (треугольник с градиентом)
        self.canvas.create_polygon(
            x, y - 55,
            x - 38, y - 20,
            x + 38, y - 20,
            fill=self.ORANGE, outline=self.WHITE, width=2
        )
        
        # Волосы - дополнительные детали
        self.canvas.create_polygon(
            x - 20, y - 55,
            x - 35, y - 25,
            x - 15, y - 30,
            fill='#CC7700', outline=''
        )
        self.canvas.create_polygon(
            x + 20, y - 55,
            x + 35, y - 25,
            x + 15, y - 30,
            fill='#CC7700', outline=''
        )
        
        # Глаза (большие и выразительные)
        eye_y = y - 15
        # Белки глаз
        self.canvas.create_oval(x - 18, eye_y - 8, x - 2, eye_y + 8, 
                               fill=self.WHITE, outline='#000000', width=1)
        self.canvas.create_oval(x + 2, eye_y - 8, x + 18, eye_y + 8, 
                               fill=self.WHITE, outline='#000000', width=1)
        
        # Зрачки
        self.canvas.create_oval(x - 15, eye_y - 3, x - 7, eye_y + 5, 
                               fill='#000000', outline='')
        self.canvas.create_oval(x + 7, eye_y - 3, x + 15, eye_y + 5, 
                               fill='#000000', outline='')
        
        # Блики в глазах
        self.canvas.create_oval(x - 12, eye_y - 1, x - 9, eye_y + 2, 
                               fill=self.WHITE, outline='')
        self.canvas.create_oval(x + 9, eye_y - 1, x + 12, eye_y + 2, 
                               fill=self.WHITE, outline='')
        
        # Нос
        self.canvas.create_polygon(x, y - 5, x - 3, y + 5, x + 3, y + 5, 
                                  fill='#CCAA88', outline='')
        
        # Рот (улыбка)
        self.canvas.create_arc(x - 12, y + 5, x + 12, y + 22, start=0, extent=180, 
                              outline=self.WHITE, width=2)
        
        # Борода/усы
        self.canvas.create_line(x - 5, y + 8, x - 15, y + 12, fill='#996633', width=2)
        self.canvas.create_line(x + 5, y + 8, x + 15, y + 12, fill='#996633', width=2)
        
        # Имя над магом (с тенью)
        self.canvas.create_text(x + 1, y - 95, text=name, fill='#000000', 
                               font=("Arial", 14, "bold"))
        self.canvas.create_text(x, y - 96, text=name, fill=light_color, 
                               font=("Arial", 14, "bold"))
        
        # Щит если есть (красивый эффект)
        if has_shield:
            # Внешний круг щита (свечение)
            self.canvas.create_oval(x - 90, y - 90, x + 90, y + 90, 
                                   outline=self.YELLOW, width=2)
            self.canvas.create_oval(x - 88, y - 88, x + 88, y + 88, 
                                   outline='#FFFF66', width=1)
            # Символ щита
            self.canvas.create_text(x, y + 5, text="⬟", fill=self.YELLOW, 
                                   font=("Arial", 50, "bold"))
        
        # HP полоска (красная)
        hp_y = y + 85
        self.draw_gradient_bar(x - 75, hp_y, 150, 18, hp, max_hp, 
                              self.GREEN if hp > max_hp * 0.5 else self.RED, "HP")
        
        # Mana полоска (синяя)
        mana_y = hp_y + 25
        self.draw_gradient_bar(x - 75, mana_y, 150, 18, mana, max_mana, 
                              self.BLUE, "MP")
        
        # Статус внизу
        status_text = "⚡ ЖИВОЙ" if hp > 0 else "☠ МЕРТВ"
        status_color = self.GREEN if hp > 0 else self.RED
        self.canvas.create_text(x, mana_y + 35, text=status_text, 
                               fill=status_color, font=("Arial", 11, "bold"))
    
    def draw_action_log(self, action_text, effect_text=""):
        """Красивый лог действия в центре с анимированной рамкой"""
        log_y = 450
        
        # Фон для текста с градиентом
        self.canvas.create_rectangle(100, log_y - 30, self.width - 100, log_y + 90, 
                                    fill='#1a0a2e', outline='#FF00FF', width=3)
        
        # Внутренняя декоративная рамка
        self.canvas.create_rectangle(105, log_y - 25, self.width - 105, log_y + 85, 
                                    fill='', outline='#00FFFF', width=1)
        
        # Основной текст действия (большой и яркий)
        self.canvas.create_text(self.width//2, log_y + 10, text=action_text, 
                               fill=self.YELLOW, font=("Arial", 16, "bold"))
        
        # Дополнительный текст (слабее)
        if effect_text:
            self.canvas.create_text(self.width//2, log_y + 50, text=effect_text, 
                                   fill=self.ORANGE, font=("Arial", 12))
    
    def draw_battle_info(self, turn, max_turns):
        """Информация о бое вверху"""
        # Заголовок
        self.canvas.create_text(self.width//2, 30, text="⚔️ БИТВА МАГОВ ⚔️", fill=self.YELLOW, font=("Arial", 20, "bold"))
        
        # Счётчик ходов
        self.canvas.create_rectangle(20, 55, 180, 85, fill=self.GRAY, outline=self.BLUE, width=2)
        progress = (turn / max_turns) * 150
        self.canvas.create_rectangle(25, 60, 25 + progress, 80, fill=self.BLUE)
        self.canvas.create_text(100, 70, text=f"Ход: {turn}/{max_turns}", fill=self.WHITE, font=("Courier", 11, "bold"))
    
    def clear_canvas(self):
        """Очистить canvas"""
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.BG)
    
    def draw_background(self):
        """Нарисовать красивый фон один раз"""
        # Основной фон
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.BG)
        
        # Градиент-подобный эффект (рисуем полоски разной интенсивности)
        for i in range(0, self.height, 20):
            opacity = '#1a1f3f' if (i // 20) % 2 == 0 else self.BG
            self.canvas.create_rectangle(0, i, self.width, i + 20, fill=opacity, outline='')
        
        # Красивая сетка
        for i in range(0, self.width, 80):
            self.canvas.create_line(i, 0, i, self.height, fill='#1a2d4d', dash=(2, 4), width=1)
        for i in range(0, self.height, 80):
            self.canvas.create_line(0, i, self.width, i, fill='#1a2d4d', dash=(2, 4), width=1)
        
        # Декоративная линия по центру
        self.canvas.create_line(self.width//2, 0, self.width//2, self.height, 
                               fill='#444466', dash=(8, 8), width=2)
    
    def render_battle_state(self, env, action_text="", effect_text=""):
        """Отрисовка боя без полной очистки экрана"""
        self.clear_canvas()
        
        # Рисуем красивый фон
        self.draw_background()
        
        # Рисуем информацию боя
        self.draw_battle_info(env.turn, env.max_turns)
        
        # Рисуем магов слева и справа
        self.draw_mage(200, 250, "🧙 АГЕНТ", env.agent.hp, env.agent.max_hp,
                      env.agent.mana, env.agent.max_mana, is_agent=True, has_shield=env.agent.shield)
        
        self.draw_mage(self.width - 200, 250, "🧙 ВРАГ", env.enemy.hp, env.enemy.max_hp,
                      env.enemy.mana, env.enemy.max_mana, is_agent=False, has_shield=env.enemy.shield)
        
        # Рисуем лог действия
        if action_text or effect_text:
            self.draw_action_log(action_text, effect_text)
        
        self.root.update()
    
    def animate_spell_effect(self, from_x, to_x, spell_name, color):
        """Анимация полёта спелла с частицами"""
        start_time = time.time()
        duration = 0.5
        
        while time.time() - start_time < duration and self.running:
            progress = (time.time() - start_time) / duration
            current_x = from_x + (to_x - from_x) * progress
            # Парабола - спелл летит по дуге
            current_y = 250 - 80 * (1 - abs(progress - 0.5) * 2)
            
            # Обновляем экран вместо полной перезарисовки
            self.canvas.delete("spell_effect")
            
            # Сам спелл (несколько кругов для эффекта)
            size = 15 + 8 * progress
            
            # Внешний светящийся круг
            self.canvas.create_oval(current_x - size - 5, current_y - size - 5,
                                   current_x + size + 5, current_y + size + 5,
                                   fill='', outline=color, width=2, tags="spell_effect")
            
            # Основной спелл
            self.canvas.create_oval(current_x - size, current_y - size,
                                   current_x + size, current_y + size,
                                   fill=color, outline=self.WHITE, width=2, tags="spell_effect")
            
            # Внутренний блик
            self.canvas.create_oval(current_x - size + 3, current_y - size + 3,
                                   current_x - size + 8, current_y - size + 8,
                                   fill=self.WHITE, outline='', tags="spell_effect")
            
            # Хвост спелла (частицы)
            tail_x = from_x + (to_x - from_x) * max(0, progress - 0.15)
            tail_y = 250 - 80 * (1 - abs(max(0, progress - 0.15) - 0.5) * 2)
            
            for i in range(3):
                offset = i * 8
                self.canvas.create_oval(tail_x - 3 - offset, tail_y - 2,
                                       tail_x + 3 - offset, tail_y + 2,
                                       fill=color, outline='', tags="spell_effect")
            
            # Название спелла над ним
            self.canvas.create_text(current_x, current_y - size - 15, text="✨",
                                   font=("Arial", 20), tags="spell_effect")
            
            self.root.update()
            time.sleep(0.02)
    
    def show_impact_effect(self, x, y, color):
        """Эффект взрыва при попадании спелла"""
        import math
        for frame in range(8):
            self.canvas.delete("impact")
            
            radius = 10 + frame * 15
            # Волны от взрыва
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                   outline=color, width=max(1, 2 - frame // 4), tags="impact")
            
            # Частицы
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad)
                self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3,
                                       fill=color, outline='', tags="impact")
            
            self.root.update()
            time.sleep(0.05)
        
        self.canvas.delete("impact")
    
    def play_battle(self, env, agent, speed=0.5):
        """Проиграть один бой"""
        state = env.reset()
        done = False
        turn_count = 0
        
        while not done and self.running:
            turn_count += 1
            
            # Действие агента
            action = agent.get_best_action(state)
            spell_name = SPELLS[action].name
            spell = SPELLS[action]
            
            # Определяем цвет спелла
            if "Fire" in spell_name:
                spell_color = self.ORANGE
                emoji = "🔥"
            elif "Big" in spell_name:
                spell_color = self.YELLOW
                emoji = "💥"
            elif "Heal" in spell_name:
                spell_color = self.GREEN
                emoji = "💚"
            elif "Shield" in spell_name:
                spell_color = self.BLUE
                emoji = "⬟"
            else:
                spell_color = self.PURPLE
                emoji = "⚡"
            
            # Показываем действие
            action_text = f"{emoji} Агент использует: {spell_name}"
            self.render_battle_state(env, action_text, "Подготовка спелла...")
            time.sleep(speed * 0.2)
            
            # Анимация полёта (если атака)
            if "Heal" not in spell_name and "Recharge" not in spell_name:
                self.animate_spell_effect(200, self.width - 200, spell_name, spell_color)
                # Эффект попадания в противника
                self.show_impact_effect(self.width - 200, 250, spell_color)
            
            # Показываем применение
            self.render_battle_state(env, action_text, "⚡ Применено!")
            time.sleep(speed * 0.15)
            
            # Делаем шаг
            next_state, reward, done, _ = env.step(action)
            
            # Показываем результат
            if env.enemy.hp <= 0:
                effect_text = f"🎯 КРИТИЧЕСКИЙ УДАР! Враг повержен!"
            elif env.agent.hp <= 0:
                effect_text = f"💔 ПОЛУЧЕН УРОН! Агент ранен!"
            else:
                effect_text = f"⚔️ Агент {int(env.agent.hp)}/100 HP  ← Враг {int(env.enemy.hp)}/100 HP"
            
            self.render_battle_state(env, action_text, effect_text)
            time.sleep(speed * 0.3)
            
            state = next_state
        
        if not self.running:
            return False
        
        # Финальное состояние
        if env.agent.is_alive() and not env.enemy.is_alive():
            result_text = "✓✓✓ АГЕНТ ПОБЕДИЛ! ✓✓✓"
            result_color = self.GREEN
            celebration_emoji = "🎉"
        elif not env.agent.is_alive() and env.enemy.is_alive():
            result_text = "✗✗✗ АГЕНТ РАЗБИТ! ✗✗✗"
            result_color = self.RED
            celebration_emoji = "💀"
        else:
            result_text = "~ НИЧЬЯ ~"
            result_color = self.WHITE
            celebration_emoji = "⚔️"
        
        # Показываем результат с красивой анимацией (пульсирование)
        pulse_frames = int(1.5 / speed)
        for blink in range(pulse_frames):
            self.clear_canvas()
            self.draw_background()
            
            self.draw_battle_info(env.turn, env.max_turns)
            self.draw_mage(200, 250, "🧙 АГЕНТ", env.agent.hp, env.agent.max_hp,
                          env.agent.mana, env.agent.max_mana, is_agent=True, has_shield=env.agent.shield)
            self.draw_mage(self.width - 200, 250, "🧙 ВРАГ", env.enemy.hp, env.enemy.max_hp,
                          env.enemy.mana, env.enemy.max_mana, is_agent=False, has_shield=env.enemy.shield)
            
            # Пульсирующий результат с размером
            pulse_size = 28 + 5 * abs(2 - (blink % 4))
            self.canvas.create_text(self.width//2, self.height//2 - 50, 
                                   text=celebration_emoji, font=("Arial", pulse_size))
            self.canvas.create_text(self.width//2, self.height//2 + 20, text=result_text, 
                                   fill=result_color, font=("Arial", 32, "bold"))
            
            self.root.update()
            time.sleep(speed * 0.3)
        
        return True
    
    def show_stats(self, win_count, loss_count, total_battles):
        """Финальная статистика"""
        self.clear_canvas()
        
        # Красивый фон
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.DARK_PURPLE)
        
        # Заголовок
        self.canvas.create_text(self.width//2, 80, text="📊 СТАТИСТИКА ДЕМОНСТРАЦИИ 📊", 
                               fill=self.YELLOW, font=("Arial", 22, "bold"))
        
        # Линия
        self.canvas.create_line(100, 120, self.width - 100, 120, fill=self.BLUE, width=2)
        
        # Статистика
        stats = [
            (f"Всего боев:", total_battles, self.WHITE),
            (f"Побед:", win_count, self.GREEN),
            (f"Поражений:", loss_count, self.RED),
            (f"Win Rate:", f"{win_count/total_battles*100:.1f}%", self.YELLOW),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            y = 200 + i * 80
            # Лейбл
            self.canvas.create_text(self.width//2 - 200, y, text=label, fill=self.WHITE, font=("Arial", 16, "bold"))
            # Значение с рамкой
            self.canvas.create_rectangle(self.width//2, y - 25, self.width//2 + 200, y + 25, 
                                        fill=self.GRAY, outline=color, width=2)
            self.canvas.create_text(self.width//2 + 100, y, text=str(value), fill=color, font=("Arial", 18, "bold"))
        
        # Закрытие
        self.canvas.create_line(100, self.height - 100, self.width - 100, self.height - 100, fill=self.BLUE, width=2)
        self.canvas.create_text(self.width//2, self.height - 40, text="Закройте окно для выхода", 
                               fill=self.WHITE, font=("Arial", 12))
        
        self.root.update()
    
    def play_multiple_battles(self, num_battles=5, speed=0.3):
        """Проиграть несколько боев"""
        agent = load_agent()
        if agent is None:
            print("❌ Не найден обученный агент!")
            return
        
        env = MageBattle()
        
        win_count = 0
        loss_count = 0
        battle_num = 0
        
        for battle_num in range(1, num_battles + 1):
            if not self.running:
                break
            
            if not self.play_battle(env, agent, speed=speed):
                break
            
            if env.agent.is_alive() and not env.enemy.is_alive():
                win_count += 1
            else:
                loss_count += 1
        
        # Финальная статистика
        if self.running:
            self.show_stats(win_count, loss_count, battle_num)
            
            # Ждем закрытия окна
            while self.running:
                self.root.update()
                time.sleep(0.1)


def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("⚔️  БИТВА МАГОВ - КРАСИВАЯ ВИЗУАЛИЗАЦИЯ  ⚔️")
    print("="*60)
    print("Загружаем обученного агента...")
    print()
    
    print("Выбираю скорость боя:")
    print("1. Медленно (1 сек на ход)")
    print("2. Нормально (0.5 сек на ход)")
    print("3. Быстро (0.2 сек на ход)")
    print()
    
    speed_choice = input("Выбор (1-3, по умолчанию 2): ").strip()
    if speed_choice == "1":
        speed = 1.0
    elif speed_choice == "3":
        speed = 0.2
    else:
        speed = 0.5
    
    num_battles = input("Сколько боев показать (по умолчанию 3): ").strip()
    if num_battles.isdigit():
        num_battles = int(num_battles)
    else:
        num_battles = 3
    
    print()
    print("Запускаем визуальную демонстрацию...")
    print("Закройте окно чтобы выйти")
    print()
    
    visualizer = MageBattleVisualizer(width=1200, height=700)
    visualizer.play_multiple_battles(num_battles=num_battles, speed=speed)
    
    print("\n✓ Визуальная демонстрация завершена!")
    print()


if __name__ == "__main__":
    main()
