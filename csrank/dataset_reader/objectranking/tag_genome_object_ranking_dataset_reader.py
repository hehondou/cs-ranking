from csrank.constants import OBJECT_RANKING
from csrank.util import scores_to_rankings
from ..tag_genome_reader import TagGenomeDatasetReader


class TagGenomeObjectRankingDatasetReader(TagGenomeDatasetReader):
    def __init__(self, dataset_type="similarity", **kwargs):
        super(TagGenomeObjectRankingDatasetReader, self).__init__(learning_problem=OBJECT_RANKING, **kwargs)
        dataset_func_dict = {"similarity": self.make_similarity_based_dataset,
                             "nearest_neighbour": self.make_nearest_neighbour_dataset,
                             "critique_fit_less": self.make_critique_fit_dataset(direction=-1),
                             "critique_fit_more": self.make_critique_fit_dataset(direction=1)}
        if dataset_type not in dataset_func_dict.keys():
            dataset_type = "similarity"

        self.dataset_function = dataset_func_dict[dataset_type]

    def make_similarity_based_dataset(self, n_instances, n_objects, seed=42, **kwargs):
        X, scores = super().make_similarity_based_dataset(n_instances=n_instances, n_objects=n_objects, seed=seed)
        # Higher the similarity lower the rank of the object
        Y = scores_to_rankings(scores)
        return X, Y

    def make_nearest_neighbour_dataset(self, n_instances, n_objects, seed, **kwargs):
        X, scores = super().make_nearest_neighbour_dataset(n_instances=n_instances, n_objects=n_objects, seed=seed)
        # Higher the similarity lower the rank of the object
        Y = scores_to_rankings(scores)
        return X, Y

    def make_critique_fit_dataset(self, direction):
        def dataset_generator(n_instances, n_objects, seed, **kwargs):
            X, scores = super(TagGenomeObjectRankingDatasetReader, self).make_critique_fit_dataset(
                n_instances=n_instances, n_objects=n_objects, seed=seed, direction=direction)
            Y = scores_to_rankings(scores)
            return X, Y

        return dataset_generator
