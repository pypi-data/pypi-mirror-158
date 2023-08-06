import warnings

import numpy as np
from gensim.models.fasttext import FastTextKeyedVectors, ft_ngram_hashes

from quantitizer import quantitize

EPSILON = 1e-24


def quantitize_ft(ft, sub_size, mode="cpu", n_iter=5):
    if mode == "cpu":
        ft_q = make_new_fasttext_model(
            ft, quantitize(ft.vectors, sub_size=sub_size, n_iter=n_iter),
            quantitize(ft.vectors_ngrams, sub_size=sub_size, n_iter=n_iter))
    elif mode == "cuda":
        from quantitizer.cuda import quantitize_cuda

        ft_q = make_new_fasttext_model(
            ft, quantitize_cuda(ft.vectors, sub_size=sub_size, n_iter=n_iter),
            quantitize_cuda(ft.vectors_ngrams, sub_size=sub_size, n_iter=n_iter))
    else:
        raise ValueError("mode must be 'cpu' or 'cuda'")

    return ft_q


def load_ft(path):
    ft = CompressedFastTextKeyedVectors.load(path)
    return ft


# This took from repo https://github.com/avidale/compress-fasttext (David Dale)


def make_new_fasttext_model(
        ft,
        new_vectors,
        new_vectors_ngrams,
        new_vocab=None,
        cls=None,
):
    cls = cls or CompressedFastTextKeyedVectors
    # let the model be the ultimate type before saving+loading it
    # cls = cls or gensim.models.fasttext.FastTextKeyedVectors
    new_ft = cls(
        vector_size=ft.vector_size,
        min_n=ft.min_n,
        max_n=ft.max_n,
        bucket=new_vectors_ngrams.shape[0],
    )
    new_ft.vectors_vocab = None  # if we don't fine tune the model we don't need these vectors
    new_ft.vectors = new_vectors  # quantized vectors top_vectors
    if new_vocab is None:
        new_ft.key_to_index = ft.key_to_index
    else:
        new_ft.key_to_index = new_vocab
    new_ft.vectors_ngrams = new_vectors_ngrams

    if hasattr(new_ft, 'update_index2word'):
        new_ft.update_index2word()

    return new_ft


class CompressedFastTextKeyedVectors(FastTextKeyedVectors):
    """ This class extends FastTextKeyedVectors by fixing several issues:
        - index2word of a freshly created model is initialized from its vocab
        - the model does not keep heavy and useless vectors_ngrams_norm
        - word_vec() method with use_norm applies normalization in the right place
    """

    def __init__(self, *args, **kwargs):
        super(CompressedFastTextKeyedVectors, self).__init__(*args, **kwargs)
        self.update_index2word()

    @classmethod
    def load(cls, *args, **kwargs):
        try:
            loaded = super(CompressedFastTextKeyedVectors, cls).load(*args, **kwargs)
        except Exception as e:
            warnings.warn(
                'You seem to be loading an old model (compressed with gensim<4.0.0, compress-fasttext<0.1.0) '
                'within an new environment (gensim>=4.0.0, compress-fasttext>=0.1.0), which may not work. '
                'Please downgrade the packages or re-compress the model within the new environment.'
            )
            raise e
        # print(loaded.__dict__)
        return make_new_fasttext_model(
            loaded,
            new_vectors=loaded.vectors,
            new_vectors_ngrams=loaded.vectors_ngrams,
            new_vocab=loaded.key_to_index,
            cls=cls,
        )

    def update_index2word(self):
        if not self.index_to_key:
            inverse_index = {value: key for key, value in self.key_to_index.items()}
            self.index_to_key = [inverse_index.get(i) for i in range(len(self.key_to_index))]

    def word_vec(self, word, use_norm=False):
        """Get `word` representations in vector space, as a 1D numpy array.
        Parameters
        ----------
        word : str
            Input word
        use_norm : bool, optional
            If True - resulting vector will be L2-normalized (unit euclidean length).
        Returns
        -------
        numpy.ndarray
            Vector representation of `word`.
        Raises
        ------
        KeyError
            If word and all ngrams not in vocabulary.
        """
        if word in self.key_to_index:
            return super(FastTextKeyedVectors, self).word_vec(word, use_norm)
        elif self.bucket == 0:
            raise KeyError('cannot calculate vector for OOV word without ngrams')
        else:
            word_vec = np.zeros(self.vectors_ngrams.shape[1], dtype=np.float32)
            ngram_hashes = ft_ngram_hashes(word=word, minn=self.min_n, maxn=self.max_n, num_buckets=self.bucket)
            if len(ngram_hashes) == 0:
                return word_vec
            for nh in ngram_hashes:
                word_vec += self.vectors_ngrams[nh]
            result = word_vec / len(ngram_hashes)
            if use_norm:
                result /= np.sqrt(max(sum(result ** 2), EPSILON))
            return result

    def fill_norms(self, force=False):
        """
        Ensure per-vector norms are available.
        Any code which modifies vectors should ensure the accompanying norms are
        either recalculated or 'None', to trigger a full recalculation later on-request.
        """
        if self.norms is None or force:
            # self.norms = np.linalg.norm(self.vectors, axis=1)
            self.norms = np.stack([sum(self.vectors[i] ** 2) ** 0.5 for i in range(len(self.vectors))])

    def init_sims(self, replace=False):
        """Precompute L2-normalized vectors.
        Parameters
        ----------
        replace : bool, optional
            If True - forget the original vectors and only keep the normalized ones = saves lots of memory!
        """
        super(FastTextKeyedVectors, self).init_sims(replace)
        # todo: make self.vectors_norm a view over self.vectors, to avoid decompression
        # do NOT calculate vectors_ngrams_norm; using them is a mistake
        self.vectors_ngrams_norm = None

    def adjust_vectors(self):
        # do not need adjusting vectors, because `vectors` instead of `vectors_vocab` are saved
        pass

    def recalc_char_ngram_buckets(self):
        # do not need calculating buckets, because `vectors` are already computed
        pass

    def _save_specials(self, fname, separately, sep_limit, ignore, pickle_protocol, compress, subname):
        """Arrange any special handling for the gensim.utils.SaveLoad protocol"""
        # don't ignore `vectors`, because they should be saved instead of `vectors_vocab`
        ignore = set(ignore).union(['buckets_word', ])
        return super(FastTextKeyedVectors, self)._save_specials(
            fname, separately, sep_limit, ignore, pickle_protocol, compress, subname
        )
