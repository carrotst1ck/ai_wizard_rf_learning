# ============================================================================
# demo.py - Демонстрационный бой обученного агента
# ============================================================================
from env import MageBattle, SPELLS
from train import load_agent


def play_demo_battle(num_battles=5):
    """
    Запустить num_battles демонстрационных боев
    Агент использует только exploit (не исследует)
    """
    
    # Загружаем обученного агента
    agent = load_agent()
    if agent is None:
        return
    
    print()
    print("="*60)
    print("ДЕМОНСТРАЦИЯ ОБУЧЕННОГО АГЕНТА")
    print("="*60)
    print()
    
    env = MageBattle()
    
    total_wins = 0
    total_losses = 0
    
    for battle_num in range(1, num_battles + 1):
        print(f"--- БОЙ #{battle_num} ---")
        print()
        
        state = env.reset()
        done = False
        
        while not done:
            # Агент использует лучшее известное действие (pure exploit)
            action = agent.get_best_action(state)
            
            # Делаем шаг в среде
            next_state, reward, done, _ = env.step(action)
            
            # Выводим информацию о ходе
            spell_name = SPELLS[action].name
            agent_hp = env.agent.hp
            agent_mana = env.agent.mana
            enemy_hp = env.enemy.hp
            enemy_mana = env.enemy.mana
            
            print(f"Ход {env.turn}: Агент использует {spell_name}")
            print(f"  Агент: HP={agent_hp}/100, Mana={agent_mana}/100", end="")
            if env.agent.shield:
                print(" [ЩИТ]", end="")
            print()
            print(f"  Враг:  HP={enemy_hp}/100, Mana={enemy_mana}/100", end="")
            if env.enemy.shield:
                print(" [ЩИТ]", end="")
            print()
            print()
            
            state = next_state
        
        # Результат боя
        if env.agent.is_alive() and not env.enemy.is_alive():
            print("✓ АГЕНТ ПОБЕДИЛ!\n")
            total_wins += 1
        elif not env.agent.is_alive() and env.enemy.is_alive():
            print("✗ АГЕНТ ПРОИГРАЛ\n")
            total_losses += 1
        else:
            print("~ НИЧЬЯ\n")
        
        print("="*60)
        print()
    
    # Финальная статистика
    print("ИТОГИ ДЕМОНСТРАЦИИ")
    print("="*60)
    print(f"Всего боев: {num_battles}")
    print(f"Побед: {total_wins} ({total_wins/num_battles*100:.0f}%)")
    print(f"Поражений: {total_losses} ({total_losses/num_battles*100:.0f}%)")
    print()


if __name__ == "__main__":
    play_demo_battle(num_battles=5)
