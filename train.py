
import os
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from env import MageBattle, NUM_ACTIONS
from agent import QLearningAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def plot_training_stats(episode_rewards, win_rates, total_episodes):
    """
    Нарисовать графики прогресса обучения
    
    Args:
        episode_rewards: лист наград за каждый эпизод
        win_rates: лист win rates (100 эпизодов)
        total_episodes: всего эпизодов обучения
    """
    
    print("\n" + "="*60)
    print("СОЗДАНИЕ ГРАФИКОВ ОБУЧЕНИЯ...")
    print("="*60 + "\n")
    
    # Создаем фигуру с 2 подграфиками
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Прогресс обучения RL-агента "Битва магов"', fontsize=16, fontweight='bold')
    
    # График 1: Win Rate
    win_rate_episodes = [i * 100 for i in range(1, len(win_rates) + 1)]
    axes[0].plot(win_rate_episodes, win_rates, 'b-', linewidth=2, label='Win Rate')
    axes[0].fill_between(win_rate_episodes, win_rates, alpha=0.3)
    axes[0].set_xlabel('Эпизод', fontsize=12)
    axes[0].set_ylabel('Win Rate (%)', fontsize=12)
    axes[0].set_title('Процент побед во время обучения', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='lower right')
    axes[0].set_ylim([0, 105])
    
    # График 2: Средняя награда
    # Вычисляем скользящую среднюю каждые 100 эпизодов
    moving_avg_rewards = []
    window = 100
    for i in range(0, len(episode_rewards), window):
        avg = sum(episode_rewards[i:i+window]) / min(window, len(episode_rewards) - i)
        moving_avg_rewards.append(avg)
    
    reward_episodes = [i * 100 for i in range(1, len(moving_avg_rewards) + 1)]
    axes[1].plot(reward_episodes, moving_avg_rewards, 'g-', linewidth=2, label='Средняя награда (скользящая)')
    axes[1].fill_between(reward_episodes, moving_avg_rewards, alpha=0.3, color='green')
    axes[1].set_xlabel('Эпизод', fontsize=12)
    axes[1].set_ylabel('Средняя награда', fontsize=12)
    axes[1].set_title('Награда за 100 боев (скользящая средняя)', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='lower right')
    
    plt.tight_layout()
    
    # Сохраняем график в папку static
    os.makedirs(STATIC_DIR, exist_ok=True)
    graph_path = os.path.join(STATIC_DIR, 'training_progress.png')
    plt.savefig(graph_path, dpi=100, bbox_inches='tight')
    print(f"✓ График сохранен в {graph_path}")
    
    # Закрываем график
    plt.close()
    
    print()


def train_agent(num_episodes=1000, verbose_interval=100, show_plot=True):
    """
    Обучить Q-learning агента через num_episodes боев
    
    Args:
        num_episodes: количество боев для обучения
        verbose_interval: выводить статистику каждые N эпизодов
        show_plot: показать ли графики после обучения
    """
    
    print("="*60)
    print("НАЧАЛО ОБУЧЕНИЯ RL-АГЕНТА")
    print("="*60)
    print(f"Количество боёв: {num_episodes}")
    print(f"Система вознаграждений включена")
    print()
    
    agent = QLearningAgent(
        num_actions=NUM_ACTIONS,
        learning_rate=0.1,      # alpha
        discount_factor=0.95,   # gamma
        epsilon=1.0             # start
    )
    
    env = MageBattle()
    
    # Статистика для отслеживания прогресса
    win_count = 0
    loss_count = 0
    draw_count = 0
    total_rewards = 0
    total_turns = 0
    episode_rewards = []
    win_rates = []
    
    # Основной цикл обучения
    for episode in range(1, num_episodes + 1):
        # Начинаем новый бой
        state = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            # Агент выбирает действие с epsilon-greedy стратегией
            action = agent.get_action(state)
            
            # Делаем шаг в среде
            next_state, reward, done, _ = env.step(action)
            
            # Обновляем Q-таблицу
            agent.update_q_value(state, action, reward, next_state, done)
            
            episode_reward += reward
            state = next_state
        
        # Снижаем epsilon (меньше случайный поиск, больше эксплуатация)
        agent.decay_epsilon()
        
        # Собираем статистику
        total_rewards += episode_reward
        total_turns += env.turn
        episode_rewards.append(episode_reward)
        
        if env.agent.is_alive() and not env.enemy.is_alive():
            win_count += 1
        elif not env.agent.is_alive() and env.enemy.is_alive():
            loss_count += 1
        else:
            draw_count += 1
        
        # Выводим прогресс
        if episode % verbose_interval == 0 or episode == 1:
            current_win_rate = win_count / episode * 100
            win_rates.append(current_win_rate)
            avg_reward = total_rewards / episode
            avg_turns = total_turns / episode
            
            print(f"[Эпизод {episode}/{num_episodes}]")
            print(f"  Win Rate: {current_win_rate:.1f}% "
                  f"(Победы: {win_count}, Поражения: {loss_count}, Ничьи: {draw_count})")
            print(f"  Средняя награда: {avg_reward:.2f}")
            print(f"  Средняя длина боя: {avg_turns:.1f} ходов")
            print(f"  Epsilon: {agent.epsilon:.4f}")
            print(f"  Q-таблица размер: {len(agent.q_table)} состояний\n")
    
    # Финальная статистика
    final_win_rate = win_count / num_episodes * 100
    avg_reward = total_rewards / num_episodes
    avg_turns = total_turns / num_episodes
    
    print("="*60)
    print("ОБУЧЕНИЕ ЗАВЕРШЕНО")
    print("="*60)
    print(f"Финальная Win Rate: {final_win_rate:.1f}%")
    print(f"Победы: {win_count}, Поражения: {loss_count}, Ничьи: {draw_count}")
    print(f"Средняя награда за бой: {avg_reward:.2f}")
    print(f"Средняя длина боя: {avg_turns:.1f} ходов")
    print(f"Размер Q-таблицы: {len(agent.q_table)} состояний")
    print()
    
    # Сохраняем Q-таблицу
    q_table_path = os.path.join(BASE_DIR, 'q_table.pkl')
    with open(q_table_path, 'wb') as f:
        pickle.dump(agent.q_table, f)
    print(f"✓ Q-таблица сохранена в {q_table_path}")
    print()
    
    # Показываем графики если requested
    if show_plot:
        plot_training_stats(episode_rewards, win_rates, num_episodes)
    
    return agent, episode_rewards, win_rates


def load_agent():
    """Загрузить обученного агента из файла"""
    try:
        q_table_path = os.path.join(BASE_DIR, 'q_table.pkl')
        with open(q_table_path, 'rb') as f:
            q_table = pickle.load(f)
        
        agent = QLearningAgent(num_actions=NUM_ACTIONS)
        agent.q_table = q_table
        agent.epsilon = 0.0  # Без случайного поиска при демонстрации
        return agent
    except FileNotFoundError:
        print("❌ Файл q_table.pkl не найден")
        print("Сначала обучите агента: python train.py")
        return None


if __name__ == "__main__":
    # Запуск обучения
    agent, episode_rewards, win_rates = train_agent(num_episodes=2000)
