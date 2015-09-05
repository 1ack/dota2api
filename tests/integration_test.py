from unittest import TestCase
from dota2api import *
import utils
from dota2api.src.urls import *
from dota2api.src.exceptions import *
from dota2api.obj.league import *
from dota2api.obj.history import *
from dota2api.obj.item import *
from dota2api.obj.detail import *
from dota2api.obj.player import *


class APITest(TestCase):
    def setUp(self):
        self.executor = utils.RequestMock()
        self.api = Initialise(executor=self.executor)

    def test_api_authentication_error(self):
        self.executor.configure_authentication_error()
        self.assertRaises(APIAuthenticationError, self.api.get_match_history)

        self.api.executor.assert_called()

    def test_api_timeout_error(self):
        self.executor.configure_timeout_error()
        self.assertRaises(APITimeoutError, self.api.get_match_history)

        self.api.executor.assert_called()

    def test_get_match_history_test(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_HISTORY,
                                   utils.LANGUAGE_PAR,
                                   'account_id=None',
                                   utils.STEAM_ID_PAR,
                                   'format=json')
        self.executor.url_matcher = matcher
        self.executor.configure_get_match_history_result()

        history = self.api.get_match_history()

        self.api.executor.assert_called()

        self.assertEqual(type(history), HistoryMatches)

        self.assertEqual(history.num_results, 10)
        self.assertEqual(history.total_results, 500)
        self.assertEqual(history.results_remaining, 490)
        self.assertEqual(len(history.matches), 10)

        self.assertEqual(type(history.matches[0]), HistoryMatch)

        self.assertEqual(history.matches[0].match_id, 1356101552)
        self.assertEqual(history.matches[0].match_seq_num, 1216063230)
        self.assertEqual(history.matches[0].start_time, 1427552454)
        self.assertEqual(history.matches[0].lobby_type, 7)
        self.assertEqual(history.matches[0].lobby_name, 'Ranked')
        self.assertEqual(history.matches[0].radiant_team_id, 0)
        self.assertEqual(history.matches[0].dire_team_id, 0)

        self.assertEqual(type(history.matches[0].players[0]), HistoryPlayer)
        self.assertEqual(history.matches[0].players[0].account_id, 140250400)
        self.assertEqual(history.matches[0].players[0].hero.id, 22)
        self.assertEqual(history.matches[0].players[0].hero.localized_name, 'Zeus')
        self.assertEqual(history.matches[0].players[0].hero.name, 'npc_dota_hero_zuus')
        self.assertEqual(history.matches[0].players[0].hero.url_full_portrait,
                         'http://cdn.dota2.com/apps/dota2/images/heroes/zuus_full.png')
        self.assertEqual(history.matches[0].players[0].hero.url_large_portrait,
                         'http://cdn.dota2.com/apps/dota2/images/heroes/zuus_lg.png')
        self.assertEqual(history.matches[0].players[0].hero.url_small_portrait,
                         'http://cdn.dota2.com/apps/dota2/images/heroes/zuus_sb.png')
        self.assertEqual(history.matches[0].players[0].hero.url_vertical_portrait,
                         'http://cdn.dota2.com/apps/dota2/images/heroes/zuus_vert.jpg')

    def test_get_match_history_by_sequence_num(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_HISTORY_BY_SEQ_NUM,
                                   utils.LANGUAGE_PAR,
                                   'start_at_match_seq_num=None',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_match_history_by_sequence_num_result()

        history = self.api.get_match_history_by_seq_num()

        self.executor.assert_called()

        self.assertEqual(type(history), HistoryMatches)
        self.assertEqual(len(history.matches), 100)

        self.assertEqual(type(history.matches[0]), HistoryMatch)
        self.assertEqual(history.matches[0].match_id, 496)
        self.assertEqual(history.matches[0].match_seq_num, 240)
        self.assertEqual(history.matches[0].start_time, 1299121489)
        self.assertEqual(history.matches[0].lobby_type, 0)
        self.assertEqual(history.matches[0].lobby_name, 'Public matchmaking')
        self.assertEqual(history.matches[0].radiant_team_id, None)
        self.assertEqual(history.matches[0].dire_team_id, None)

        self.assertEqual(type(history.matches[0].players[0]), HistoryPlayer)

        self.assertEqual(history.matches[0].players[0].account_id, 4294967295)
        self.assertEqual(history.matches[0].players[0].hero.id, 18)
        self.assertEqual(history.matches[0].players[0].hero.localized_name, 'Sven')

    def test_get_match_details(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_DETAILS,
                                   utils.LANGUAGE_PAR,
                                   'match_id=123',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_single_match_result()

        history = self.api.get_match_details(123)

        self.executor.assert_called()

        self.assertEqual(type(history), DetailMatch)
        self.assertEqual(history.lobby_name, u"Public matchmaking")
        self.assertEqual(history.game_mode_name, u"All Pick")
        self.assertEqual(history.cluster_name, "South America")
        self.assertEqual(history.is_radiant_win, True)

        self.assertEqual(type(history.players[0]), DetailMatchPlayer)
        self.assertEqual(history.players[0].account_id, 170086708)
        self.assertEqual(history.players[0].player_slot, 0)
        self.assertEqual(history.players[0].kills, 12)
        self.assertEqual(history.players[0].deaths, 7)
        self.assertEqual(history.players[0].assists, 14)
        self.assertEqual(history.players[0].leaver_status.id, 0)
        self.assertEqual(history.players[0].leaver_status.name, 'NONE')
        self.assertEqual(history.players[0].leaver_status.description, 'finished match, no abandon')
        self.assertEqual(history.players[0].last_hits, 241)
        self.assertEqual(history.players[0].denies, 1)
        self.assertEqual(history.players[0].gold_per_min, 572)
        self.assertEqual(history.players[0].xp_per_min, 694)
        self.assertEqual(history.players[0].gold_spent, 23110)
        self.assertEqual(history.players[0].hero_damage, 16022)
        self.assertEqual(history.players[0].tower_damage, 2261)
        self.assertEqual(history.players[0].hero_healing, 0)
        self.assertEqual(history.players[0].level, 24)
        self.assertEqual(history.players[0].hero_damage, 16022)

        self.assertEqual(type(history.players[0].hero), Hero)
        self.assertEqual(history.players[0].hero.localized_name, "Legion Commander")
        self.assertEqual(history.players[1].hero.localized_name, "Omniknight")
        self.assertEqual(history.players[2].hero.localized_name, "Templar Assassin")
        self.assertEqual(history.players[3].hero.localized_name, "Lion")
        self.assertEqual(history.players[4].hero.localized_name, "Chaos Knight")
        self.assertEqual(history.players[5].hero.localized_name, "Sven")
        self.assertEqual(history.players[6].hero.localized_name, "Disruptor")
        self.assertEqual(history.players[7].hero.localized_name, "Lone Druid")
        self.assertEqual(history.players[8].hero.localized_name, "Terrorblade")
        self.assertEqual(history.players[9].hero.localized_name, "Timbersaw")

        self.assertEqual(type(history.players[0].items[0]), Item)
        self.assertEqual(history.players[0].items[0].id, 127)
        self.assertEqual(history.players[0].items[0].localized_name, 'Blade Mail')
        self.assertEqual(history.players[0].items[1].id, 168)
        self.assertEqual(history.players[0].items[1].localized_name, 'Desolator')
        self.assertEqual(history.players[0].items[2].id, 1)
        self.assertEqual(history.players[0].items[2].localized_name, 'Blink Dagger')
        self.assertEqual(history.players[0].items[3].id, 158)
        self.assertEqual(history.players[0].items[3].localized_name, 'Mjollnir')
        self.assertEqual(history.players[0].items[4].id, 112)
        self.assertEqual(history.players[0].items[4].localized_name, 'Assault Cuirass')
        self.assertEqual(history.players[0].items[5].id, 63)
        self.assertEqual(history.players[0].items[5].localized_name, 'Power Treads')

        self.assertEqual(type(history.players[0].ability_upgrades[0]), AbilityUpgrade)
        self.assertEqual(history.players[0].ability_upgrades[0].ability, 5597)
        self.assertEqual(history.players[0].ability_upgrades[0].ability_name, 'legion_commander_moment_of_courage')
        self.assertEqual(history.players[0].ability_upgrades[0].level, 1)
        self.assertEqual(history.players[0].ability_upgrades[0].time, 130)

        self.assertEqual(history.players[1].ability_upgrades[1].ability, 5265)
        self.assertEqual(history.players[1].ability_upgrades[1].ability_name, 'omniknight_degen_aura')
        self.assertEqual(history.players[1].ability_upgrades[1].level, 2)
        self.assertEqual(history.players[1].ability_upgrades[1].time, 318)

        self.assertEqual(len(history.players[7].additional_units), 1)
        self.assertEqual(history.players[7].additional_units[0].items[0].id, 158)
        self.assertEqual(history.players[7].additional_units[0].items[0].localized_name, 'Mjollnir')

    def test_get_league_listing(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_LEAGUE_LISTING,
                                   utils.LANGUAGE_PAR,
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_league_listing_result()

        history = self.api.get_league_listing()

        self.executor.assert_called()

        self.assertEqual(type(history), LeagueListing)
        self.assertEqual(len(history), 931)

        self.assertEqual(type(history[0]), League)
        self.assertEqual(history[0].league_id, 1212)
        self.assertEqual(history[0].name, 'Dota 2 Just For Fun')
        self.assertEqual(history[0].tournament_url, 'https://binarybeast.com/xDOTA21404228/')
        self.assertEqual(history[0].description, "64 of the best Brazilian amateur teams compete to become" +
                                                 " the winner of the first Dota 2 Just For Fun tournament. ")

        self.assertEqual(history[0].itemdef, 10541)

    def test_get_live_league_games(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_LIVE_LEAGUE_GAMES,
                                   utils.LANGUAGE_PAR,
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_live_league_games_result()

        history = self.api.get_live_league_games()

        self.executor.assert_called()

        self.assertEqual(type(history), LiveLeagueGames)
        self.assertEqual(len(history), 5)

        self.assertEqual(type(history[0]), LiveLeagueGame)
        self.assertEqual(type(history[0].radiant_team), LiveLeagueGameTeam)
        self.assertEqual(history[0].radiant_team.team_name, 'Stroy Bat')
        self.assertEqual(history[0].radiant_team.team_id, 1734383)
        self.assertEqual(history[0].radiant_team.team_logo, 46500877983858209)
        self.assertEqual(history[0].radiant_team.complete, False)

        self.assertEqual(type(history[0].scoreboard), LiveLeagueGameScoreboard)
        self.assertEqual(history[0].scoreboard.roshan_respawn_timer, 0)
        self.assertEqual(history[0].scoreboard.duration, 2335.81787109375)

        self.assertEqual(type(history[0].scoreboard.radiant), LiveLeagueGameTeamScoreboard)
        self.assertEqual(history[0].scoreboard.radiant.score, 19)
        self.assertEqual(history[0].scoreboard.radiant.tower_state, 1796)
        self.assertEqual(history[0].scoreboard.radiant.barracks_state, 51)

        self.assertEqual(type(history[0].scoreboard.radiant.picks[0]), Hero)
        self.assertEqual(history[0].scoreboard.radiant.picks[0].id, 95)
        self.assertEqual(history[0].scoreboard.radiant.picks[0].localized_name, 'Troll Warlord')

        self.assertEqual(type(history[0].scoreboard.radiant.bans[0]), Hero)
        self.assertEqual(history[0].scoreboard.radiant.bans[0].id, 17)
        self.assertEqual(history[0].scoreboard.radiant.bans[0].localized_name, 'Storm Spirit')

        self.assertEqual(type(history[0].scoreboard.radiant.players[0]), LiveLeagueGamePlayer)
        self.assertEqual(history[0].scoreboard.radiant.players[0].player_slot, 1)
        self.assertEqual(history[0].scoreboard.radiant.players[0].account_id, 193496070)

        self.assertEqual(type(history[0].scoreboard.radiant.players[0].hero), Hero)
        self.assertEqual(history[0].scoreboard.radiant.players[0].hero.id, 84)

        self.assertEqual(history[0].scoreboard.radiant.players[0].kills, 3)
        self.assertEqual(history[0].scoreboard.radiant.players[0].deaths, 5)
        self.assertEqual(history[0].scoreboard.radiant.players[0].assists, 9)
        self.assertEqual(history[0].scoreboard.radiant.players[0].last_hits, 61)
        self.assertEqual(history[0].scoreboard.radiant.players[0].denies, 5)
        self.assertEqual(history[0].scoreboard.radiant.players[0].gold, 366)
        self.assertEqual(history[0].scoreboard.radiant.players[0].level, 16)
        self.assertEqual(history[0].scoreboard.radiant.players[0].gold_per_min, 255)
        self.assertEqual(history[0].scoreboard.radiant.players[0].xp_per_min, 381)
        self.assertEqual(history[0].scoreboard.radiant.players[0].ultimate_state, 3)
        self.assertEqual(history[0].scoreboard.radiant.players[0].ultimate_cooldown, 0)
        self.assertEqual(history[0].scoreboard.radiant.players[0].respawn_timer, 0)
        self.assertEqual(history[0].scoreboard.radiant.players[0].position_x, -5192.20263671875)
        self.assertEqual(history[0].scoreboard.radiant.players[0].position_y, -4190.29638671875)
        self.assertEqual(history[0].scoreboard.radiant.players[0].net_worth, 7166)

        self.assertEqual(type(history[0].scoreboard.radiant.players[0].items[0]), Item)
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[0].id, 0)
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[0].localized_name, '')
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[1].id, 60)
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[1].localized_name, 'Point Booster')
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[2].id, 46)
        self.assertEqual(history[0].scoreboard.radiant.players[0].items[2].localized_name, 'Town Portal Scroll')

    def test_get_team_info_by_team_id(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_TEAM_INFO_BY_TEAM_ID,
                                   utils.LANGUAGE_PAR,
                                   'start_at_team_id=1778397',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_team_info_by_team_id()

        history = self.api.get_team_info_by_team_id(1778397)

        self.executor.assert_called()

        self.assertEqual(type(history), Teams)
        self.assertEqual(len(history), 100)

        self.assertEqual(type(history[0]), Team)
        self.assertEqual(history[0].team_id, 1778397)
        self.assertEqual(history[0].name, 'Athletic`S')
        self.assertEqual(history[0].tag, 'A`S')
        self.assertEqual(history[0].time_created, 1406576259)
        self.assertEqual(history[0].rating, 'inactive')
        self.assertEqual(history[0].logo, 25098200687093967)
        self.assertEqual(history[0].logo_sponsor, 0)
        self.assertEqual(history[0].url, '')
        self.assertEqual(history[0].games_played_with_current_roster, 0)
        self.assertEqual(history[0].player_0_account_id, 45983302)
        self.assertEqual(history[0].player_1_account_id, 89990613)
        self.assertEqual(history[0].player_2_account_id, 93972394)
        self.assertEqual(history[0].player_3_account_id, 128939846)
        self.assertEqual(history[0].player_4_account_id, None)
        self.assertEqual(history[0].player_5_account_id, None)
        self.assertEqual(history[0].player_4_account_id, None)
        self.assertEqual(history[0].player_6_account_id, None)
        self.assertEqual(history[0].admin_account_id, 45983302)

    def test_get_player_summaries(self):
        steam_cdn = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/'
        matcher = utils.UrlMatcher(BASE_URL + GET_PLAYER_SUMMARIES,
                                   utils.LANGUAGE_PAR,
                                   'steamids=%5B76561198049003839%5D',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_player_summaries()

        history = self.api.get_player_summaries(convert_to_64_bit(88738111))

        self.executor.assert_called()

        self.assertEqual(type(history), PlayerSummaries)
        self.assertEqual(len(history), 1)

        self.assertEqual(type(history[0]), PlayerSummary)
        self.assertEqual(history[0].steam_id, '76561198049003839')
        self.assertEqual(history[0].community_visibility_state, 3)
        self.assertEqual(history[0].profile_state, 1)
        self.assertEqual(history[0].persona_name, 'Bogs')
        self.assertEqual(history[0].last_logoff, 1429074263)
        self.assertEqual(history[0].profile_url, 'http://steamcommunity.com/profiles/76561198049003839/')
        self.assertEqual(history[0].url_avatar,
                         steam_cdn + 'images/avatars/28/28d9341fc54980fb28946201944ddab438a27a59.jpg')
        self.assertEqual(history[0].url_avatar_medium,
                         steam_cdn + 'images/avatars/28/28d9341fc54980fb28946201944ddab438a27a59_medium.jpg')
        self.assertEqual(history[0].url_avatar_full,
                         steam_cdn + 'images/avatars/28/28d9341fc54980fb28946201944ddab438a27a59_full.jpg')
        self.assertEqual(history[0].persona_state, 0)
        self.assertEqual(history[0].primary_clan_id, '103582791432815637')
        self.assertEqual(history[0].time_created, 1316303056)
        self.assertEqual(history[0].persona_state_flags, 0)

    def test_get_heroes(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_HEROES,
                                   utils.LANGUAGE_PAR,
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_heroes()

        history = self.api.get_heroes()

        self.executor.assert_called()

        self.assertEqual(len(history), 110)
        self.assertEqual(history[0].name, 'npc_dota_hero_antimage')
        self.assertEqual(history[0].id, 1)
        self.assertEqual(history[0].localized_name, 'Anti-Mage')

    def test_get_game_items(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_GAME_ITEMS,
                                   utils.LANGUAGE_PAR,
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_game_items()

        history = self.api.get_game_items()

        self.executor.assert_called()

        self.assertEqual(len(history), 237)
        self.assertEqual(history[0].id, 1)
        self.assertEqual(history[0].name, 'item_blink')
        self.assertEqual(history[0].cost, 2250)
        self.assertEqual(history[0].is_recipe, False)
        self.assertEqual(history[0].in_side_shop, True)
        self.assertEqual(history[0].in_secret_shop, False)
        self.assertEqual(history[0].localized_name, 'Blink Dagger')
        self.assertEqual(history[0].url_image, 'http://cdn.dota2.com/apps/dota2/images/items/blink_lg.png')

    def test_get_tournament_prize_pool(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_TOURNAMENT_PRIZE_POOL,
                                   utils.LANGUAGE_PAR,
                                   'leagueid=1778397',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_tournament_prize_pool()

        history = self.api.get_tournament_prize_pool(1778397)

        self.executor.assert_called()

        self.assertEqual(history.prize_pool, 0)
        self.assertEqual(history.league_id, 1778397)

    def test_get_match_details_ranked(self):
        matcher = utils.UrlMatcher(BASE_URL + GET_MATCH_DETAILS,
                                   utils.LANGUAGE_PAR,
                                   'match_id=321',
                                   utils.STEAM_ID_PAR,
                                   'format=json')

        self.executor.url_matcher = matcher
        self.executor.configure_get_match_details_ranked()

        history = self.api.get_match_details(321)

        self.executor.assert_called()

        self.assertEqual(history.game_mode, 22)
        self.assertEqual(history.game_mode_name, "All Pick")
        self.assertEqual(history.lobby_type, 7)
        self.assertEqual(history.lobby_name, "Ranked")
