from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# will create a default user to test data and persmission
main_user = User(id=1, name="Test User", email="coloed3@gmail.com")
session.add(main_user)

""" 
creating the fake data for our database, working on collecting descriptions
sports 
"""
category1 = Category(id=1, name='Football')
category2 = Category(id=2, name='League of Legends')
category3 = Category(id=3, name='Biking')
category4 = Category(id=4, name='Skeet Shooting')
category5 = Category(id=5, name='Bowling')
category6 = Category(id=6, name='Volleyball')
category7= Category(id=7, name='Skiing')
category8 = Category(id=8, name='Handball')
category9 = Category(id=9, name='Powerlifting')
category10 = Category(id=10, name='Track')


# add the above tot he tables
session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.add(category6)
session.add(category7)
session.add(category8)
session.add(category9)
session.add(category10)


# will allow for the below to add id, name and deescripptio


item1 = Item(id=1, name='Padding',
             description="""The first football shoulder pads were created by Princeton student L.P. Smock in 1877. 
             These were made of leather and wool and were thin, light, and did not provide much protection. Additionally,
              they were sewn into the players' jerseys rather than being worn as a separate piece of equipment""",
             category=category1,
             user=main_user)
item2 = Item(id=2, name='Football',
             description="""The oldest football still in existence, which is thought to have been made circa 1550,
              was discovered in the roof of Stirling Castle, Scotland, in 1981""",
             category=category1,
             user=main_user)
item3 = Item(id=3, name='National Football Leauge',
             description="""s a professional American football league consisting of 32 teams, divided equally 
             between the National Football Conference (NFC) and the American Football Conference (AFC).
              The NFL is one of the four major professional sports leagues in North America,
               and the highest professional level of American football in the world.[3] 
               The NFL's 17-week regular season runs from early September 
               to late December, with each team playing 16 games 
               and having one bye week. Following the conclusion 
               of the regular season, six teams from each conference 
               (four division winners and two wild card teams) advance to the playoffs, 
               a single-elimination tournament culminating in the Super Bowl, 
             which is usually held in the first Sunday in February, 
             and is played between the champions of the NFC and AFC. """,
             category=category1,
             user=main_user)

item4 = Item(id=4, name='League Of Legends',
             description="""league of legends is a online game that consist of 2 teams with 5 players going
             5v5 on the map summoners rift. the Intent of the game is to take the others team nexus """,
             category=category2,
             user=main_user)

item5 = Item(id=5, name='LOL Esports',
             description='is a series of tournements held through out the world, to gain higher rankings',
             category=category2,
             user=main_user)

item6 = Item(id=6, name='Bikes',
             description='''There are many brands of bikes, from Trek to Mongoose determing the right one will be 
              best way to see which bike allows for speed and ease of use''',
             category=category3,
             user=main_user)

item7 = Item(id=7, name='Rifles',
             description='''skeet shoowing requires, the right gun and alot of amo''',
             category=category4,
             user=main_user)
item8 = Item(id=8, name='Winchester SXP trap',
             description='Ranked one of the top 10 best all round trap shooting shotguns',
             category=category4,
             user=main_user)

item9 = Item(id=9, name='Brunswick Rhino Reactive',
             description='''Best ball for dry lanes''',
             category=category5,
             user=main_user)
item10 = Item(id=10, name='Hammer Black Widow',
              description='''Best ball for heavy oil lanes ''',
              category=category5,
              user=main_user)

item11 = Item(id=11, name='Puredrop Volleyball trainer',
              description='Allows the user to learn how to do a 1 on 1 serve with no reset',
              category=category6,
              user=main_user)
item12 = Item(id=12, name='Mikasa MGV500 Heavy',
              description='Official weight and size ball for professional volley ball tournments',
              category=category6,
              user=main_user)
item13 = Item(id=13, name='Mizuno Womens wave',
              description='Considered one of the best volley balls shoes for women',
              category=category6,
              user=main_user)

item14 = Item(id=14, name='Volki 90Eight',
              description='Speed, weight, one of the best rated skis used for professional made by professionals.',
              category=category7,
              user=main_user)
item15 = Item(id=15, name='Ski-doo BV25',
              description='Head gear, used for pro skking',
              category=category7,
              user=main_user)

item16 = Item(id=16, name='molten Eleit Handball',
              description='Offical handball of the international handball federation IHF',
              category=category8,
              user=main_user)

item17 = Item(id=17, name='Squat Rack',
              description='a piece of equipment used for squats ,deadlifts, bench essential to powerlifting training',
              category=category9,
              user=main_user)
item18 = Item(id=18, name='Chains',
              description='''Heavy chains prompt more weight and use of stability muscles''',
              category=category9,
              user=main_user)
item19 = Item(id=19, name='Usain Bolt',
              description='A powered suppliment for runners',
              category=category10,
              user=main_user)
item20 = Item(id=20, name='Nike Air jumps',
              description='best used for running outside for track',
              category=category10,
              user=main_user)


session.add(item1)
session.add(item2)
session.add(item3)
session.add(item4)
session.add(item5)
session.add(item6)
session.add(item7)
session.add(item8)
session.add(item9)
session.add(item10)
session.add(item11)
session.add(item12)
session.add(item13)
session.add(item14)
session.add(item15)
session.add(item16)
session.add(item17)
session.add(item18)
session.add(item19)
session.add(item20)

session.commit()

print('ALl items have been added to the database')