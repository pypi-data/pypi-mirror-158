import egene_main as egene
import time

# Calico Benchmarking
# Inital Time: 1.101 seconds with 100000 calicos
# Shortend active layers [BROKE CODE]: .61746777
# Less shortend active layers: 0.98612356
# Indexing Edges by pnode layer at begining of feedforward: 0.8555827600000001
# Indexing Edges by pnode layer when Network is initalized: 0.68477302
# Collecting output layer more explictily: 0.65733014
# Faster setting of input layer: 0.65637152
# Using node layer starts in _feedforward_calculate: 0.62797408

ins = [[3, 5, 2], [8, 4, 2], [1, 3, 5], [6, 3, 2]]
outs = [[20], [28], [18], [22]]

s_guy = [-0.10051578645070869, 0.6797641917191805, 0.5343263253202423, -0.5863544590777034, -0.5675438619266051, -0.5966373068987143, 0.29896275603106437, -0.9888740352281457, -0.317194274354211, -0.2655820762006891, -0.3119928081750897, -0.46536851710972615, 0.9200209586723679, -0.9284506296918966, -0.47096272937122263, 0.9971721133966918]

spec = egene.Species([3, 3, 1], ins, outs, initial_weights=s_guy)
guy = spec.networks[0]



total_time = 0
test_number = 5

for _ in range(test_number):
    t_start = time.time_ns()
    for _ in range(100000):
        guy.calico([4, 3, 2])
    t_end = time.time_ns()
    t_delta_seconds = (t_end - t_start) / 1000000000
    total_time += t_delta_seconds
    print("Calico test:", t_delta_seconds)

print("AVERAGE TIME:", total_time / test_number)
