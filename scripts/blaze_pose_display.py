import collections
import typing as tp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas
import collections

def get_chain_dots(
        dots: np.ndarray,   # shape == (n_dots, 3)
        chain_dots_indexes: tp.List[int], # length == n_dots_in_chain
                                          # in continuous order, i.e. 
                                          # left_hand_ix >>> chest_ix >>> right_hand_ix
        ) -> np.ndarray:    # chain of dots
    """Get continuous chain of dots
    
    chain_dots_indexes - 
        indexes of points forming a continuous chain;
        example of chain: [hand_l, elbow_l, shoulder_l, chest, shoulder_r, elbow_r, hand_r]
    """
    # print(chain_dots_indexes)
    # print(dots) 
    return dots[chain_dots_indexes]

def get_chains(
        dots: np.ndarray,   # shape == (n_dots, 3)
        left_elbow_wrist_chain_ixs: tp.List[int],
        right_elbow_wrist_chain_ixs: tp.List[int],
        left_shoulder_elbow_chain_ixs: tp.List[int],
        right_shoulder_elbow_chain_ixs: tp.List[int],
        left_hips_knee_ixs: tp.List[int],
        right_hips_knee_ixs: tp.List[int],
        left_knee_ankle_ixs: tp.List[int],
        right_knee_ankle_ixs: tp.List[int],
        left_right_shoulder_ixs: tp.List[int],
        left_right_hip_ixs: tp.List[int],
        left_right_shoulder_hip_ixs: tp.List[int]
        ):
    return (get_chain_dots(dots, left_elbow_wrist_chain_ixs),
            get_chain_dots(dots, right_elbow_wrist_chain_ixs),
            get_chain_dots(dots, left_shoulder_elbow_chain_ixs),
            get_chain_dots(dots, right_shoulder_elbow_chain_ixs),
            get_chain_dots(dots, left_hips_knee_ixs),
            get_chain_dots(dots, right_hips_knee_ixs),
            get_chain_dots(dots, left_knee_ankle_ixs),
            get_chain_dots(dots, right_knee_ankle_ixs),
            get_chain_dots(dots, left_right_shoulder_ixs),
            get_chain_dots(dots, left_right_hip_ixs),
            get_chain_dots(dots, left_right_shoulder_hip_ixs))


def subplot_nodes(dots: np.ndarray, # shape == (n_dots, 3)
                  ax):
    return ax.scatter3D(*dots.T, c=dots[:, -1])


def subplot_bones(chains: tp.Tuple[np.ndarray, ...], ax):
    return [ax.plot(*chain.T) for chain in chains]


def plot_skeletons(
        skeletons: tp.Sequence[np.ndarray], 
        chains_ixs: tp.Tuple[tp.List[int], tp.List[int], tp.List[int]],
        key):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    def animate(i):
        ax.clear()
        dots = skeletons[i]
        chains = get_chains(dots, *chains_ixs)
        subplot_nodes(dots, ax)
        subplot_bones(chains, ax)
        return ax

    def init():
        dots = skeletons[0]
        chains = get_chains(dots, *chains_ixs)
        
        subplot_nodes(dots, ax)
        subplot_bones(chains, ax)
        return ax
    
    anim = FuncAnimation(fig, animate, init_func=init,
                               frames=len(skeletons), interval=100)

    anim.save('./gifs/' + key + '.gif', writer='imagemagick', fps=10)



def test():
    df = pandas.read_csv('pose-output.csv')

    data_dict = {}
    for index, row in df.iterrows():
        name = row['name']
        if name in data_dict:
            for i in range(1, 100):
                if name + '_' + str(i) not in  data_dict:
                    name = name + '_' + str(i)
                    break
        data_dict[name] = df.loc[index, df.columns != 'name']

    data_dict_final = collections.defaultdict(list)

    for key in data_dict:
        for c in data_dict[key]:
            data_dict_final[key].append([float(i) for i in c.strip('][').split(', ')])

    """Plot random poses of simplest skeleton"""
    for key in data_dict_final:
        try:
            data = data_dict_final[key]
            skeletons = []
            skeleton = None
            for i in range(120):
                l = 0
                skeleton = []
                for k in range(12):
                    skeleton.append([])
                    for t in range(3):
                        skeleton[-1].append(data[k * 3 + t][i])
                left_shoulder = skeleton[0]
                right_shoulder = skeleton[1]
                left_hip = skeleton[6]
                right_hip = skeleton[7]
                head_arr = []
                mid_hip_arr = []
                for t in range(3):
                    head = (left_shoulder[t] + right_shoulder[t]) / 2
                    mid_hip = (left_hip[t] + right_hip[t]) / 2
                    head_arr.append(head)
                    mid_hip_arr.append(mid_hip)
                skeleton.append(head_arr)
                skeleton.append(mid_hip_arr)
                # print(np.array([skeleton]))
                skeletons.append(skeleton)
                # print(skeleton)
            
            skeletons = np.array(skeletons)
            chains_ixs = (
                        [2, 4],  # left_elbow, left_wrist
                        [3, 5],    # right_elbow, right_wrist
                        [0, 2],    # left_shoulder, left_elbow
                        [1, 3],    # right_shoulder, right_elbow
                        [6, 8],    # left_hip, left_knee
                        [7, 9],    # right_hip, right_knee
                        [8, 10],    # left_knee, left_ankle
                        [9, 11],    # right_knee, right_ankle
                        [0, 1],     # left_shoulder, right_shoulder
                        [6, 7],      # left_hip, right_hip,
                        [12, 13]     # head, mid_hip
                )
            plot_skeletons(skeletons, chains_ixs, key)
        except:
            continue


if __name__ == '__main__':

    test()