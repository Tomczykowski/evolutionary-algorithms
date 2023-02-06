import random
import timeit


def create_full_graph(number_of_vertex):
    graph = []
    for i in range(number_of_vertex - 1):
        for j in range(i+1, number_of_vertex):
            graph.append([i, j])
    return graph


def del_edges_from_graph(number_of_vertex, number_of_edges_to_del):
    graph = create_full_graph(number_of_vertex)
    for i in range(1, number_of_edges_to_del + 1):
        edge_id = random.randint(0, len(graph) - 1)
        del graph[edge_id]
    return graph


def make_base_population(size_of_population, number_of_vertices):
    base_generation = []
    for i in range(size_of_population):
        subject = []
        for j in range(number_of_vertices):
            subject.append(random.randint(0, 1))
        base_generation.append(subject)
    return base_generation


def assess_subject(subject, graph):
    subject_grade = 0
    for i in subject:
        if i == 1:
            subject_grade += 1

    for edge in graph:
        if subject[edge[0]] == 0 and subject[edge[1]] == 0:
            subject_grade += 1000
    return subject_grade


def choose_to_battle(generation):
    chosen_subjects = []
    id_of_subject_first = random.randint(0, len(generation)-1)
    id_of_subject_second = random.randint(0, len(generation)-1)
    while id_of_subject_first == id_of_subject_second:
        id_of_subject_second = random.randint(0, len(generation)-1)
    chosen_subjects.append(generation[id_of_subject_first])
    chosen_subjects.append(generation[id_of_subject_second])
    return chosen_subjects


def selection(base_generation, graph):
    next_generation = []
    for i in range(len(base_generation)):
        chosen_subjects_to_battle = choose_to_battle(base_generation)
        first_subject = chosen_subjects_to_battle[0]
        second_subject = chosen_subjects_to_battle[1]
        grade_of_first_subject = assess_subject(first_subject, graph)
        grade_of_second_subject = assess_subject(second_subject, graph)
        if grade_of_first_subject <= grade_of_second_subject:
            next_generation.append(first_subject)
        else:
            next_generation.append(second_subject)

    return next_generation


def mutating(generation):
    for subject_id in range(len(generation)):
        if random.randint(0, 100) < 100:
            for i in range(len(generation[subject_id])):
                if random.randint(0, 100) < 5:
                    if generation[subject_id][i] == 1:
                        generation[subject_id][i] = 0
                    else:
                        generation[subject_id][i] = 1
    return generation


def rating_adaptation(generation, best_subject, graph):
    best_rate = assess_subject(best_subject, graph)
    for subject in generation:
        subject_rate = assess_subject(subject, graph)
        if subject_rate < best_rate:
            best_subject = subject.copy()
            best_rate = subject_rate
    return best_subject


def evolution_algorithm(size_of_population, number_of_vertices, number_of_generation, graph):
    generation = make_base_population(size_of_population, number_of_vertices)
    best_subject = generation[0]
    for i in range(number_of_generation):
        best_subject = rating_adaptation(generation, best_subject, graph)
        generation = selection(generation, graph)
        generation = mutating(generation)
    print(assess_subject(best_subject, graph))
    return best_subject


first_graph = del_edges_from_graph(25, 150)
print(timeit.timeit(stmt="evolution_algorithm(30, 25, 800, first_graph)", globals=globals(), number=5)/5)
