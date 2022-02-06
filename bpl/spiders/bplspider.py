from unicodedata import name
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
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2021-22-1296684/match-results',
    ]

    def parse(self, response):
        for i, link in enumerate(response.css('.match-info-link-FIXTURES::attr(href)')):            
            yield response.follow(link.get(), callback=self.parse_bpl, meta={'id':i, 'r':response.url})

    def parse_bpl(self, response):
        yield {                        
            'id': int(str(self.start_urls.index(response.meta.get('r'))) + str(response.meta.get('id'))),
            'season': response.css('.match-details-table tbody tr td a::text')[2].get(),
            'match_no': response.css('.description::text').get().split(' ')[0],
            'date': response.css('.description::text').get()[-11:],
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
            'win_by_wickets': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3] if 'wickets' == ''.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[4]) else 0,
            'win_by_runs': response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3] if 'runs' == ''.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[4]) else 0,
            'result': ' '.join(response.css('.match-info.match-info-MATCH.match-info-MATCH-half-width .status-text span::text').get().split(' ')[3:5]),
            'umpire_1': response.css('.multiple-detail-table-values h5::text').get(),
            'umpire_2': response.css('.multiple-detail-table-values h5::text')[1].get(),
        }

        
class BatsmanSpider(scrapy.Spider):
    name = 'batsman'
    start_urls = [
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2011-12-547342/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2012-13-586487/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2015-16-921139/match-results',
        'https://www.espncricinfo.com/series/bpl-2016-2016-17-1063043/match-results',
        'https://www.espncricinfo.com/series/bpl-2017-2017-18-1121242/match-results',
        'https://www.espncricinfo.com/series/bpl-2018-19-1169376/match-results',    
        'https://www.espncricinfo.com/series/bpl-2020-2019-20-1207676/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2021-22-1296684/match-results',
    ]

    def parse(self, response):
        for i, link in enumerate(response.css('.match-info-link-FIXTURES::attr(href)')):       
            yield response.follow(link.get(), callback=self.parse_bpl, meta={'id':i, 'r':response.url})

    def parse_bpl(self, response):
        for tables in response.css('.batsman tbody'):
            for row in tables.css('tr')[:-1]:   
                try:                                    
                    yield{       
                        'id': int(str(self.start_urls.index(response.meta.get('r'))) + str(response.meta.get('id'))),
                        'season': response.css('.match-details-table tbody tr td a::text')[2].get(),  
                        'match_no': response.css('.description::text').get().split(' ')[0],    
                        'date': response.css('.description::text').get()[-11:],   
                        'player_name': row.css('td a::text').get(),
                        'comment': row.css('td')[1].css('td::text').get(),
                        'R': row.css('td')[2].css('td::text').get(),
                        'B': row.css('td')[3].css('td::text').get(),
                        'M': row.css('td')[4].css('td::text').get(),
                        'fours': row.css('td')[5].css('td::text').get(),
                        'sixs': row.css('td')[6].css('td::text').get(),
                        'SR': row.css('td')[7].css('td::text').get(),                   
                    }
                except:
                    pass    

class BowlerSpider(scrapy.Spider):
    name = 'bowler'
    start_urls = [
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2011-12-547342/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2012-13-586487/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2015-16-921139/match-results',
        'https://www.espncricinfo.com/series/bpl-2016-2016-17-1063043/match-results',
        'https://www.espncricinfo.com/series/bpl-2017-2017-18-1121242/match-results',
        'https://www.espncricinfo.com/series/bpl-2018-19-1169376/match-results',    
        'https://www.espncricinfo.com/series/bpl-2020-2019-20-1207676/match-results',
        'https://www.espncricinfo.com/series/bangladesh-premier-league-2021-22-1296684/match-results',
    ]

    def parse(self, response):
        for i, link in enumerate(response.css('.match-info-link-FIXTURES::attr(href)')):        
            yield response.follow(link.get(), callback=self.parse_bpl, meta={'id':i, 'r':response.url})

    def parse_bpl(self, response):
        for tables in response.css('.bowler tbody'):
            for row in tables.css('tr')[:-1]:   
                try:                                    
                    yield{       
                        'id': int(str(self.start_urls.index(response.meta.get('r'))) + str(response.meta.get('id'))),
                        'season': response.css('.match-details-table tbody tr td a::text')[2].get(),  
                        'match_no': response.css('.description::text').get().split(' ')[0],    
                        'date': response.css('.description::text').get()[-11:],   
                        'player_name': row.css('td a::text').get(),
                        'O': row.css('td')[1].css('td::text').get(),
                        'M': row.css('td')[2].css('td::text').get(),
                        'R': row.css('td')[3].css('td::text').get(),
                        'W': row.css('td')[4].css('td::text').get() or row.css('td')[4].css('td span::text').get(),
                        'ECON': row.css('td')[5].css('td::text').get(),
                        'WD': row.css('td')[9].css('td::text').get(),
                        'NB': row.css('td')[10].css('td::text').get(),                   
                    }
                except:
                    pass    

