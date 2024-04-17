# SQLLMConverter

# Basic Info:
## ec2 instance (mysql & sqlite)
- ssh -i xxx/cs511-key.pem ubuntu@ec2-18-117-190-220.us-east-2.compute.amazonaws.com 
- sudo mysql -u root
- Converter: https://github.com/techouse/sqlite3-to-mysql
- pip3 install sqlite3-to-mysql
- sudo sqlite3mysql -f ~/spider/database/academic/academic.sqlite -d academic -u root
- sudo sqlite3mysql -f ~/spider/database/bike_1/bike_1.sqlite -d bike_1 -u cs511 --mysql-password cs511password
- user: -u root -p 123456 / -u cs511 -p cs511password
- split queries: https://drive.google.com/file/d/1Bc-j40KcviE-NSM-7FRupGlyKa6j_U6c/view?usp=sharing
- mongodb migrator mongo URI:mongodb://34.70.54.136:27017 without username/password

## virtual environment activation:
```
python -m venv .venv
```
```
# windows
.venv\Scripts\activate
# mac
. .venv/bin/activate (Try windows version first. If that works, skip this. Otherwise, try this.)
```
```
pip install -r requirements.txt
```

## currently using db & tables: 
mysql: bike_1, academic
- Tables_in_bike_1 
  - station          
  - status           
  - trip             
  - weather  

- Tables_in_academic
  - author
  - conference
  - domain
  - domain_author
  - domain_conference
  - domain_journal
  - domain_keyword
  - journal
  - keyword
  - publication

mongodb: admin
- Tables_in_admin
    - author
    - conference
    - domain
    - domainAuthor
    - domainConference
    - domainJournal
    - domainKeyword
    - journal
    - keyword
    - publication
    - station
    - status
    - trip
    - weather

## Migration Status (to MySQL)
*  activity_1
*  allergy_1
*  apartment_rentals
*  assets_maintenance
*  battle_death
*  behavior_monitoring
*  bike_1
*  body_builder
*  book_2
*  browser_web
*  candidate_poll
*  chinook_1
*  cinema
*  climbing
*  club_1
*  coffee_shop
*  college_1
*  college_3
*  company_1
*  company_office
*  county_public_safety
*  course_teach
*  cre_Doc_Template_Mgt
*  cre_Doc_Tracking_DB
*  cre_Docs_and_Epenses
*  cre_Theme_park
*  csu_1
*  customer_complaints
*  customer_deliveries
*  customers_and_addresses
*  customers_and_invoices
*  customers_and_products_contacts
*  customers_campaigns_ecommerce
*  customers_card_transactions
*  debate
*  decoration_competition
*  department_management
*  department_store
*  device
*  document_management
*  dog_kennels
*  driving_school
*  e_government
*  e_learning
*  election
*  election_representative
*  entertainment_awards
*  entrepreneur
*  epinions_1
*  farm
*  film_rank
*  flight_company
*  formula_1
*  game_1
*  game_injury
*  gas_company
*  gymnast
*  icfp_1
*  insurance_and_eClaims
*  insurance_fnol
*  insurance_policies
*  journal_committee
*  local_govt_in_alabama
*  local_govt_mdm
*  manufactory_1
*  manufacturer
*  match_season
*  medicine_enzyme_interaction
*  mountain_photos
*  movie_1
*  music_2
*  music_4
*  musical
*  network_1
*  network_2
*  news_report
*  orchestra
*  party_host
*  perpetrator
*  pets_1
*  pilot_record
*  poker_player
*  product_catalog
*  products_for_hire
*  products_gen_characteristics
*  program_share
*  railway
*  real_estate_properties
*  restaurant_1
*  riding_club
*  roller_coaster
*  school_bus
*  school_player
*  scientist_1
*  ship_1
*  ship_mission
*  singer
*  small_bank_1
*  soccer_2
*  solvency_ii
*  sports_competition
*  station_weather
*  store_1
*  store_product
*  storm_record
*  student_1
*  student_transcripts_tracking
*  swimming
*  theme_gallery
*  tracking_grants_for_research
*  tracking_orders
*  tracking_share_transactions
*  tracking_software_problems
*  train_station
*  twitter_1
*  university_basketball
*  voter_2
*  wedding
*  workshop_paper
*  world_1
## 10 Chosen Dataset
*  chinook_1
*  icfp_1
*  scientist_1
*  small_bank_1
*  soccer_2
*  twitter_1
*  allergy_1
*  network_1
*  battle_death
*  swimming


