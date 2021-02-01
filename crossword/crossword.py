from collections import deque


class Cell:
    def __init__(self, i, j, cw):
        self.i = i
        self.j = j
        self.cw = cw

    def get_neigh_vectors(self):
        neigh_vectors = []
        if self.j > 0:
            if self.cw[self.i][self.j-1] != "+":
                neigh_vectors.append((0, -1))  # Left [1]
        if self.j < 9:
            if self.cw[self.i][self.j+1] != "+":
                neigh_vectors.append((0, 1))  # Right [3]
        if self.i > 0:
            if self.cw[self.i-1][self.j] != "+":
                neigh_vectors.append((-1, 0))  # Up [2]
        if self.i < 9:
            if self.cw[self.i+1][self.j] != "+":
                neigh_vectors.append((1, 0))  # Down [4]
        return neigh_vectors

    def advance(self, vector):
        self.i += vector[0]
        self.j += vector[1]

    def can_advance_with(self, vector):
        try:
            return self.cw[self.i + vector[0]][self.j + vector[1]] == "-"
        except (IndexError, TypeError):
            return False

    def is_cross(self):
        vectors = self.get_neigh_vectors()
        for i in range(0, len(vectors) - 1):
            dot_product = vectors[i][0] * vectors[i+1][0] + vectors[i][1] * vectors[i+1][1]
            if dot_product == 0:
                return True
        return False

    def get_pair(self):
        return (self.i, self.j)

    def set_pair(self, i, j):
        self.i = i
        self.j = j

    def get_content(self):
        return self.cw[self.i][self.j]

    def set_content(self, content):
        self.cw[self.i] = self.cw[self.i][:self.j] + content + self.cw[self.i][self.j+1:]


def first_cross(crossword):
    cell = Cell(0, 0, crossword)
    for i in range(10):
        for j in range(10):
            cell.set_pair(i, j)
            if cell.get_content() == "-" and cell.is_cross():
                return cell


def vector_generator():
    yield (-1, 0)  # up
    yield (1, 0)  # down
    yield (0, -1)  # left
    yield (0, 1)  # right

def get_relations(crossword):
    cell = first_cross(crossword)
    crosses = deque([cell.get_pair()])
    crosses_visited = set(crosses)
    blank_lengths = []
    blank_crosses_sets = []
    while len(crosses) > 0:
        crosses_set = {}
        length = 0
        crosses_with_new_blanks = 0
        for vector in vector_generator():
            cell.set_pair(*crosses[0])  # queue's head
            blank_id = len(blank_lengths)
            while True:
                if cell.is_cross():
                    # if cross hasn't been marked, save as cross with new blank space at current length.
                    if cell.get_content() == "-":
                        crosses_with_new_blanks += 1
                        crosses_set[blank_id + crosses_with_new_blanks] = length
                    # If it has been marked (by other blank space), save as cross with that blank space at current length.
                    elif cell.get_content() != str(blank_id):
                        crosses_set[int(cell.get_content())] = length
                    # Append to crosses in case it's not appended
                    if cell.get_pair() not in crosses_visited:
                        crosses.append(cell.get_pair())
                        crosses_visited.add(cell.get_pair())
                cell.set_content(str(blank_id))
                if cell.can_advance_with(vector):
                    cell.advance(vector)
                    length += 1
                else:
                    break

            # if vector is up or left (first pass)
            if vector == (-1, 0) or vector == (0, -1):
                for blank_id in crosses_set:
                    # adjust breakpoints gotten for current blank space
                    crosses_set[blank_id] = length - crosses_set[blank_id]
            # vector is right or down (second pass) and a new blank space was found after second pass
            elif length > 0:
                # Save and reset for each word traversed in current cross.
                blank_lengths.append(length + 1)
                blank_crosses_sets.append(crosses_set)
                length = 0
                crosses_set = {}
                crosses_with_new_blanks = 0
        crosses.popleft()  # deque current cross.

    return blank_lengths, blank_crosses_sets

def tag_words(words, blank_lengths, blank_crosses):

    tags = {}
    words_count = len(words)
    unassigned_words = set(words)
    while len(unassigned_words) > 0:
        for word_id in range(words_count):
            matched_word = ""
            for word in words:
                if len(word) == blank_lengths[word_id]:
                    for cross_word_id in blank_crosses[word_id]:
                        # Extract the indices where the cross takes place at for both of the words.
                        index_word, index_cross_word =  blank_crosses[word_id][cross_word_id], blank_crosses[cross_word_id][word_id]
                        for cross_word in words:
                            if len(cross_word) == blank_lengths[cross_word_id]:
                                # Validate that the same char is at those indices.
                                if word[index_word] == cross_word[index_cross_word]:



cw = ["+-++++++++",
      "+-++++++++",
      "+-++++++++",
      "+-----++++",
      "+-+++-++++",
      "+-+++-++++",
      "+++++-++++",
      "++------++",
      "+++++-++++",
      "+++++-++++"]

# cw = ["+-++++++++",
#       "+-++++++++",
#       "+-------++",
#       "+-++++++++",
#       "+-++++++++",
#       "+------+++",
#       "+-+++-++++",
#       "+++++-++++",
#       "+++++-++++",
#       "++++++++++"]

# cw = ["++++++-+++",
#       "++------++",
#       "++++++-+++",
#       "++++++-+++",
#       "+++------+",
#       "++++++-+-+",
#       "++++++-+-+",
#       "++++++++-+",
#       "++++++++-+",
#       "++++++++-+"]


lengths, crosses = get_relations(cw)
print(lengths)
print(crosses)
for row in cw:
    print(row)


# def crosswordPuzzle(crossword, words):
