# ============================================================================
# agent.py - Q-Learning агент
# ============================================================================
# Реализация табличного Q-learning для выбора действий в боевой среде
# ============================================================================

import random


class QLearningAgent:
    """
    Q-learning агент с:
    - Q-таблицей (state -> action -> Q-value)
    - epsilon-greedy стратегией выбора действия
    - обновлением Q-значений через Bellman equation
    """
    
    def __init__(self, num_actions, learning_rate=0.1, discount_factor=0.95, epsilon=1.0):
        """
        Args:
            num_actions: количество доступных действий (5 спеллов)
            learning_rate: alpha - как быстро учиться (0.1 хороший выбор)
            discount_factor: gamma - важность будущих наград (0.95 стандарт)
            epsilon: стартовое значение для epsilon-greedy (1.0 = полный случайный поиск)
        """
        self.num_actions = num_actions
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = 0.995  # Как быстро снижаем случайный поиск
        self.epsilon_min = 0.01  # Минимальный epsilon (всегда немного исследуем)
        
        self.q_table = {}  # Словарь: state -> {action -> q_value}
    
    def _ensure_state_in_q_table(self, state):
        """Если состояния нет в Q-таблице, добавляем его с нулевыми значениями"""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in range(self.num_actions)}
    
    def get_action(self, state):
        """
        Выбрать действие через epsilon-greedy стратегию
        
        Смысл epsilon-greedy:
        - С вероятностью epsilon: выбираем СЛУЧАЙНОЕ действие (explore)
        - С вероятностью 1-epsilon: выбираем ЛУЧШЕЕ известное действие (exploit)
        
        В начале обучения epsilon=1.0 (мы только исследуем)
        К концу epsilon≈0.01 (мы в основном эксплуатируем)
        """
        self._ensure_state_in_q_table(state)
        
        # Выбираем: исследовать или эксплуатировать?
        if random.random() < self.epsilon:
            # Исследование: случайное действие
            return random.randint(0, self.num_actions - 1)
        else:
            # Эксплуатация: лучшее известное действие
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            # Если несколько действий имеют одинаковый Q, выбираем случайное из них
            best_actions = [a for a, q in q_values.items() if q == max_q]
            return random.choice(best_actions)
    
    def update_q_value(self, state, action, reward, next_state, done):
        """
        Обновить Q-значение для пары (state, action) через Bellman equation
        
        Bellman equation:
        Q(s, a) = Q(s, a) + α * (r + γ * max_Q(s', a) - Q(s, a))
        
        Где:
        - Q(s, a) = старое Q-значение
        - α (alpha) = скорость обучения
        - r = полученная награда
        - γ (gamma) = коэффициент дисконтирования (важность будущих наград)
        - max_Q(s', a) = максимальное Q-значение в следующем состоянии
        - done = закончился ли эпизод
        
        Логика:
        Если мы получили награду r и интерпретируем будущее как max_Q(s'),
        то новое Q-значение должно быть ближе к (r + γ * max_Q(s')).
        Параметр α контролирует размер шага обновления.
        """
        self._ensure_state_in_q_table(state)
        self._ensure_state_in_q_table(next_state)
        
        old_q_value = self.q_table[state][action]
        
        if done:
            # Если бой закончился - нет будущих наград
            td_target = reward
        else:
            # Если бой продолжается - добавляем дисконтированное максимальное Q следующего состояния
            max_next_q = max(self.q_table[next_state].values())
            td_target = reward + self.gamma * max_next_q
        
        # TD error - ошибка временного разностного обучения
        td_error = td_target - old_q_value
        
        # Обновляем Q-значение
        self.q_table[state][action] = old_q_value + self.alpha * td_error
    
    def decay_epsilon(self):
        """
        Снизить epsilon после каждого эпизода
        Это означает: со временем мы меньше исследуем, больше эксплуатируем
        """
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def get_q_value(self, state, action):
        """Получить Q-значение для пары (state, action)"""
        self._ensure_state_in_q_table(state)
        return self.q_table[state][action]
    
    def get_best_action(self, state):
        """Получить лучшее действие (без случайности, pure exploitation)"""
        self._ensure_state_in_q_table(state)
        q_values = self.q_table[state]
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)
    
    def reset(self):
        """Полностью сбросить агента (для нового обучения)"""
        self.q_table = {}
        self.epsilon = 1.0
