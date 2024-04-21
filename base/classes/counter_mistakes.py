import pandas as pd
import os
import numpy as np


class CounterMistakes:
    def __init__(self, id_user):
        self.id_user = id_user;
        self.file_counter = 0
        self.mistakes_names = ["Missing abstract method implementations", "Diamond inheritance problem",
                               "Not using the super() function", "Problem with the polymorphism",
                               "Static variable issue", "Complex inheritance hierarchy"]
        self.dict_mistakes = {mistake: 0 for mistake in self.mistakes_names}
        self.tan = 0

    def count_mistakes(self, tab_topic, tab_files, tab_description):

        for i in range(len(tab_files)): self.file_counter += 1

        # based on the topic, count the number of mistakes
        for i in range(len(tab_topic)):
            self.dict_mistakes[tab_topic[i]] += 1

    def return_info(self):
        return self.dict_mistakes, self.file_counter

    def calculate_tan(self):
        # put the number of mistakes to table
        tab_mistakes = [self.dict_mistakes[mistake] for mistake in self.mistakes_names]
        # sort the table
        tab_mistakes.sort()
        # calculate tan
        y = [0] * len(tab_mistakes)
        maks = tab_mistakes[-1]
        mean = sum(tab_mistakes) / len(tab_mistakes)
        for i in range(len(tab_mistakes)):
            y[i] = (tab_mistakes[i] * (maks - mean / 2)) / self.file_counter

        # calculate best tan for x from tab_mistakes and y
        x = np.array(tab_mistakes)
        y = np.array(y)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        self.tan = numerator / denominator

    def write_to_csv(self):
        where = '../../data/user_analysis.csv'
        # create dataframe with first column id, then columns from dict_mistakes and then file_counter and then tan
        df = pd.DataFrame(columns=['id'] + self.mistakes_names + ['file_counter'] + ['tan'])
        # create first row using information
        df.loc[0] = [self.id_user] + [self.dict_mistakes[mistake] for mistake in self.mistakes_names] + [
            self.file_counter] + [self.tan]
        # if file does not exist
        if not os.path.isfile(where):
            df.to_csv(where, index=False)
        else:
            df_old = pd.read_csv(where)
            # check if user already exists
            if self.id_user in df_old['id'].values:
                # update row with user
                # add 7 rows to the row with user
                for mistake in self.mistakes_names:
                    df_old.loc[df_old['id'] == self.id_user, mistake] += df.loc[0, mistake]
                df_old.loc[df_old['id'] == self.id_user, 'file_counter'] += df.loc[0, 'file_counter']
                # update self_mistakes and file_counter
                self.file_counter = df_old.loc[df_old['id'] == self.id_user, 'file_counter'].values[0]
                for mistake in self.mistakes_names:
                    self.dict_mistakes[mistake] = df_old.loc[df_old['id'] == self.id_user, mistake].values[0]
                self.calculate_tan()
                df_old.loc[df_old['id'] == self.id_user, 'tan'] = self.tan
                df_old.to_csv(where, index=False)
            else:
                df = pd.concat([df_old, df], ignore_index=True)
                df.to_csv(where, index=False)
