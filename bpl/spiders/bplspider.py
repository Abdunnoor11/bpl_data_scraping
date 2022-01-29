import scrapy
from urllib.parse import urljoin


class BplSpider(scrapy.Spider):
    name = 'bpl'
    start_urls = [
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2011-12-547342/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2012-13-586487/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2015-16-921139/match-results',
        'https://www.espncricinfo.com/series/bpl-2016-2016-17-1063043/match-results',
        'https://www.espncricinfo.com/series/bpl-2017-2017-18-1121242/match-results',
        'https://www.espncricinfo.com/series/bpl-2018-19-1169376/match-results',    
        'https://www.espncricinfo.com/series/bpl-2020-2019-20-1207676/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2021-22-1296684/match-schedule-fixtures',
    ]

    def parse(self, response):
        for link in response.css('.match-info-link-FIXTURES::attr(href)'):            
            yield response.follow(link.get(), callback=self.parse_bpl)

    def parse_bpl(self, response):
        yield {            
            'season': response.css('.match-details-table tbody tr td a::text')[2].get(),
            'match_no': response.css('.description::text').get().split(' ')[0],
            'team_1': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .team p::text').get(),
            'team_1_score': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .team .score::text')[0].get(),
            'team_2': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .team p::text')[1].get(),
            'team_2_score': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .team .score::text')[1].get(),
            'player_of_match': response.css('.playerofthematch-name::text').get(),
            'toss_winner' : response.css('.match-details-table tbody tr td::text')[1].get().split(',')[0],
            'toss_decision' : ' '.join(response.css('.match-details-table tbody tr td::text')[1].get().split(' ')[-2:]),
            'winner': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[0],        
            'venue': response.css('.match-details-table tbody tr td a::text').get(),
            'city': response.css('.match-details-table tbody tr td a::text').get().split(' ')[-1],
            'date': response.css('.description::text').get()[-11:],
            'win_by_wickets': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3] if 'wickets' == ''.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[4]) else 0,
            'win_by_runs': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3] if 'runs' == ''.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[4]) else 0,
            'result': ' '.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3:5]),
            'umpire_1': response.css('.multiple-detail-table-values h5::text').get(),
            'umpire_2': response.css('.multiple-detail-table-values h5::text')[1].get(),
        }

        