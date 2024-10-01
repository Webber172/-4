from collections import defaultdict Изменил типо код

def rankdata(a):
    n = len(a)
    ranks = [0] * n
    sorted_indices = sorted(range(n), key=lambda i: a[i])
    
    rank = 1
    for i in range(n):
        if i > 0 and a[sorted_indices[i]] == a[sorted_indices[i - 1]]:
            ranks[sorted_indices[i]] = ranks[sorted_indices[i - 1]]
        else:
            ranks[sorted_indices[i]] = rank
        rank += 1
    ranks_sum = defaultdict(int)
    ranks_count = defaultdict(int)
    for i in range(n):
        ranks_sum[a[i]] += ranks[i]
        ranks_count[a[i]] += 1
    
    for i in range(n):
        if ranks_count[a[i]] > 1:
            ranks[i] = ranks_sum[a[i]] / ranks_count[a[i]]

    return ranks

def calculate_spearman_correlation(ratings1, ratings2):
    n = len(ratings1)
    rank1 = rankdata(ratings1)
    rank2 = rankdata(ratings2)
    d_squared_sum = sum((rank1[i] - rank2[i])**2 for i in range(n))
    return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))

def calculate_concordance(expert_ratings):
    n_experts = len(expert_ratings)
    n_objects = len(expert_ratings[0])

    ranked_ratings = []
    for expert in expert_ratings:
        ranked_ratings.append(rankdata(list(expert.values())))

    ranked_ratings = zip(*ranked_ratings)
    sum_of_squared_deviations = 0
    for obj_ranks in ranked_ratings:
        mean_rank = sum(obj_ranks) / n_experts
        sum_of_squared_deviations += sum((rank - mean_rank)**2 for rank in obj_ranks)

    return 12 * sum_of_squared_deviations / (n_experts**2 * (n_objects**3 - n_objects))

def find_inconsistent_expert(expert_ratings):
    """Находит эксперта с наибольшим количеством несогласованных оценок."""
    n_experts = len(expert_ratings)
    inconsistency_counts = [0] * n_experts

    for i in range(n_experts):
        for j in range(i + 1, n_experts):
            ratings1 = list(expert_ratings[i].values())
            ratings2 = list(expert_ratings[j].values())
            correlation = calculate_spearman_correlation(ratings1, ratings2)
            if correlation < 0.5:  
                inconsistency_counts[i] += 1
                inconsistency_counts[j] += 1

    max_inconsistency = max(inconsistency_counts)
    if max_inconsistency > 0:
        return inconsistency_counts.index(max_inconsistency)
    else:
        return None

def main():
    """Основная функция программы."""
    n_experts = int(input("Введите количество экспертов: "))
    n_indicators = int(input("Введите количество показателей: "))

    indicator_names = []
    for i in range(n_indicators):
        while True:
            indicator_name = input(f"Введите название показателя {i+1}: ")
            if indicator_name in indicator_names:
                print("Показатель уже существует, введите правильно.")
            else:
                indicator_names.append(indicator_name)
                break

    expert_ratings = []
    for i in range(n_experts):
        expert_dict = {}
        print(f"\nВведите оценки эксперта {i+1}:")
        for indicator_name in indicator_names:
            while True:
                try:
                    rating = int(input(f"{indicator_name}: "))
                    expert_dict[indicator_name] = rating
                    break
                except ValueError:
                    print("Ошибка: Введите целое число для оценки.")
        expert_ratings.append(expert_dict)

    if n_experts == 2:
        ratings1 = list(expert_ratings[0].values())
        ratings2 = list(expert_ratings[1].values())
        correlation = calculate_spearman_correlation(ratings1, ratings2)
        print("\nРанговый коэффициент корреляции Спирмена:", correlation)
        if correlation >= 0.7:
            print("Мнения экспертов согласованы.")
        else:
            print("Мнения экспертов не согласованы.")
    else:
        kendall_w = calculate_concordance(expert_ratings)
        print("\nКоэффициент конкордации Кендалла W:", kendall_w)
        if kendall_w >= 0.7:
            print("Мнения экспертов согласованы.")
        else:
            print("Мнения экспертов не согласованы.")

    if n_experts > 2:
        inconsistent_expert = find_inconsistent_expert(expert_ratings)
        if inconsistent_expert is not None:
            print("\nЭксперт с наибольшим количеством несогласованных оценок:", inconsistent_expert + 1)
        else:
            print("\nВсе эксперты полностью согласованы.")

        if kendall_w < 0.7 and inconsistent_expert is not None:
            print("\nРекомендуется заменить эксперта", inconsistent_expert + 1, "на другого эксперта.")

if __name__ == "__main__":
    main()
    
