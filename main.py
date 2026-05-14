# ============================================================================
# main.py - Главное меню проекта
# ============================================================================
import os
from train import train_agent, load_agent
from demo import play_demo_battle


def main():
    """Главное меню проекта"""
    
    while True:
        print("\n" + "="*60)
        print("БИТВА МАГОВ - RL Проект")
        print("="*60)
        print("\nВыберите действие:")
        print("1. Обучить агента с нуля (2000 боев)")
        print("2. Загрузить обученного агента и посмотреть демо")
        print("3. Выход")
        print()
        
        choice = input("Ваш выбор (1-3): ").strip()
        
        if choice == "1":
            num_episodes = input("\nКоличество боев для обучения (по умолчанию 2000): ").strip()
            if num_episodes.isdigit():
                num_episodes = int(num_episodes)
            else:
                num_episodes = 2000
            
            show_graphs = input("Показать графики обучения? (y/n, по умолчанию y): ").strip().lower()
            show_plot = show_graphs != 'n'
            
            print()
            agent, episode_rewards, win_rates = train_agent(num_episodes=num_episodes, show_plot=show_plot)
            
            # После обучения предлагаем посмотреть демо
            watch_demo = input("\nПосмотреть демо боев обученного агента? (y/n): ").strip().lower()
            if watch_demo == 'y':
                num_demos = input("Сколько боев показать в демо (по умолчанию 5): ").strip()
                if num_demos.isdigit():
                    num_demos = int(num_demos)
                else:
                    num_demos = 5
                print()
                play_demo_battle(num_battles=num_demos)
        
        elif choice == "2":
            if not os.path.exists('q_table.pkl'):
                print("\n❌ Файл q_table.pkl не найден!")
                print("Сначала обучите агента (вариант 1)")
                continue
            
            num_demos = input("\nСколько боев показать в демо (по умолчанию 5): ").strip()
            if num_demos.isdigit():
                num_demos = int(num_demos)
            else:
                num_demos = 5
            
            print()
            play_demo_battle(num_battles=num_demos)
        
        elif choice == "3":
            print("\nДо встречи! 👋")
            break
        
        else:
            print("\n❌ Некорректный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
