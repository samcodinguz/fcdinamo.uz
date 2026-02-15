from django.urls import path
from . import views

urlpatterns = [
    path('home', views.judge, name='judge'),
    path('news', views.judge_news, name='judge_news'),
    path('news/tags', views.judge_news_tags, name='judge_news_tags'),
    path('news/tags/add', views.judge_news_tags_add, name='judge_news_tags_add'),
    path('news/tags/edit/<int:tags_id>', views.judge_news_tags_edit, name='judge_news_tags_edit'),
    path('news/tags/delete/<int:tags_id>', views.judge_news_tags_delete, name='judge_news_tags_delete'),
    path('news/edit/<int:news_id>', views.judge_news_edit, name='judge_news_edit'),
    path('news/edit/add', views.judge_news_add, name='judge_news_add'),
    path('news/delete/<int:news_id>', views.judge_news_delete, name='judge_news_delete'),

    path('leagues', views.judge_leagues, name='judge_leagues'),
    path('leagues/add', views.judge_leagues_add, name='judge_leagues_add'),
    path('leagues/delete/<int:league_id>', views.judge_leagues_delete, name='judge_leagues_delete'),
    path('leagues/edit/<int:league_id>', views.judge_leagues_edit, name='judge_leagues_edit'),

    path('seasons', views.judge_seasons, name='judge_seasons'),
    path('seasons/add', views.judge_seasons_add, name='judge_seasons_add'),
    path('seasons/delete/<int:season_id>', views.judge_seasons_delete, name='judge_seasons_delete'),
    path('seasons/edit/<int:season_id>', views.judge_seasons_edit, name='judge_seasons_edit'),

    path('team/type', views.judge_team_type, name='judge_team_type'),
    path('team/type/add', views.judge_team_type_add, name='judge_team_type_add'),
    path('team/type/edit/<int:team_type_id>', views.judge_team_type_edit, name='judge_team_type_edit'),
    path('team/type/delete<int:team_type_id>', views.judge_team_type_delete, name='judge_team_type_delete'),

    path('matches', views.judge_matches, name='judge_matches'),
    path('matches/add', views.judge_matches_add, name='judge_matches_add'),
    path('matches/delete/<int:match_id>', views.judge_matches_delete, name='judge_matches_delete'),
    path('matches/edit/<int:match_id>', views.judge_matches_edit, name='judge_matches_edit'),

    path('matches/clubs', views.judge_clubs, name='judge_clubs'),
    path('matches/clubs/add', views.judge_clubs_add, name='judge_clubs_add'),
    path('matches/clubs/edit/<int:clubs_id>', views.judge_clubs_edit, name='judge_clubs_edit'),
    path('matches/clubs/delete/<int:clubs_id>', views.judge_clubs_delete, name='judge_clubs_delete'),

    path('players', views.judge_players, name='judge_players'),
    path('players/add', views.judge_players_add, name='judge_players_add'),
    path('players/position', views.judge_players_position, name='judge_players_position'),
    path('players/position/add', views.judge_players_position_add, name='judge_players_position_add'),
    path('players/position/edit/<int:position_id>', views.judge_players_position_edit, name='judge_players_position_edit'),
    path('players/position/delete/<int:position_id>', views.judge_players_position_delete, name='judge_players_position_delete'),
    path('players/edit/<int:player_id>', views.judge_players_edit, name='judge_players_edit'),
    path('players/delete/<int:player_id>', views.judge_players_delete, name='judge_players_delete'),


    path('coachs', views.judge_coachs, name='judge_coachs'),
    path('coachs/add', views.judge_coachs_add, name='judge_coachs_add'),
    path('coachs/position', views.judge_coachs_position, name='judge_coachs_position'),
    path('coachs/position/add', views.judge_coachs_position_add, name='judge_coachs_position_add'),
    path('coachs/position/edit/<int:position_id>', views.judge_coachs_position_edit, name='judge_coachs_position_edit'),
    path('coachs/position/delete/<int:position_id>', views.judge_coachs_position_delete, name='judge_coachs_position_delete'),
    path('coachs/edit/<int:coach_id>', views.judge_coachs_edit, name='judge_coachs_edit'),
    path('coachs/delete/<int:coach_id>', views.judge_coachs_delete, name='judge_coachs_delete'),


    path('managements', views.judge_managements, name='judge_managements'),
    path('managements/add', views.judge_managements_add, name='judge_managements_add'),
    path('managements/position', views.judge_managements_position, name='judge_managements_position'),
    path('managements/position/add', views.judge_managements_position_add, name='judge_managements_position_add'),
    path('managements/position/edit/<int:position_id>', views.judge_managements_position_edit, name='judge_managements_position_edit'),
    path('managements/position/delete/<int:position_id>', views.judge_managements_position_delete, name='judge_managements_position_delete'),
    path('managements/edit/<int:management_id>', views.judge_managements_edit, name='judge_managements_edit'),
    path('managements/delete/<int:management_id>', views.judge_managements_delete, name='judge_managements_delete'),

    path('club/infos', views.judge_club_infos, name='judge_club_infos'),

    path('contacts', views.judge_contacts, name='judge_contacts'),

    path('message/read/', views.mark_message_read, name='mark_message_read'),
    path('message/delete/<int:msg_id>', views.delete_message, name='delete_message'),
    path('', views.judge_galery, name='judge_galery'),
    path('video/add', views.judge_video_add, name='judge_video_add'),
    path('video/delete/<int:video_id>', views.judge_video_delete, name='judge_video_delete'),
    path('video/edit/<int:video_id>', views.judge_video_edit, name='judge_video_edit'),
]