from nba_api.stats.endpoints import leagueleaders
import random

class NBAStatsGame:
    def __init__(self, stat_categories):
        self.stat_categories = stat_categories
        self.selection_pool = []
        self.all_ranks = {}
        self.current_category = ''

    def fetch_all_players(self, stat_category, min_games=50):
        data = leagueleaders.LeagueLeaders(
            season='2023-24',
            season_type_all_star='Regular Season',
            stat_category_abbreviation=stat_category,
            per_mode48='PerGame'
        ).get_normalized_dict()['LeagueLeaders']

        return [
            {'PLAYER_ID': player['PLAYER_ID'], 'PLAYER': player['PLAYER'], f'{stat_category}_RANK': player['RANK']}
            for player in data if player['GP'] >= min_games
        ]

    def sort_players_by_rank(self, player):
        return player[f'{self.current_category}_RANK']

    def get_selection_pool_and_all_ranks(self):
        for cat in self.stat_categories:
            self.current_category = cat
            all_players = self.fetch_all_players(cat)
            top_30_players = sorted(all_players, key=self.sort_players_by_rank)[:30]

            for player in top_30_players:
                if player['PLAYER_ID'] not in [p['PLAYER_ID'] for p in self.selection_pool]:
                    self.selection_pool.append(player)

            for player in all_players:
                if player['PLAYER_ID'] not in self.all_ranks:
                    self.all_ranks[player['PLAYER_ID']] = {'PLAYER': player['PLAYER']}
                self.all_ranks[player['PLAYER_ID']][f'{cat}_RANK'] = player[f'{cat}_RANK']
