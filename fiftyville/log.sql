-- Keep a log of any SQL queries you execute as you solve the mystery.
.schema --know the data availble
SELECT description FROM crime_scene_reports where month = 7 AND day = 28 AND year = 2021 AND street = 'Humphrey Street'; --know what happened at the scene and wether there were witnesses
SELECT transcript, name FROM interviews where month = 7 AND day = 28 AND year = 2021;
SELECT activity, license_plate FROM bakery_security_logs where month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute >= 15 AND minute <=25; --knowing who left the bakery right after the crime was comitted 5P2BI95
SELECT caller, receiver, duration FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller where people.license_plate = '6P58WS2';--to check licens plates left after robbery duration phonecalls
SELECT license_plate, atm_transactions.transaction_type, atm_transactions.amount from people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number where atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.year = 2021 AND atm_transactions.atm_location = 'Leggett Street';--to check which licence plate withdrew money
SELECT hour, minute,airports.full_name FROM flights JOIN airports ON airports.id = flights.origin_airport_id where month = 7 AND day = 29 AND year = 2021;--CHECKING EARLIEST FLIGHTS
SELECT license_plate FROM people JOIN flights ON flights.id = passengers.flight_id where flights.month = 7 AND flights.day = 29 AND flights.year = 2021 AND flights.hour=8;--know the criminal
SELECT name from people where people.license_plate = '94KL13X';
SELECT hour, minute,airports.full_name FROM flights JOIN airports ON airports.id = flights.destination_airport_id where month = 7 AND day = 29 AND year = 2021;--know destination
SELECT caller, receiver, duration FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller where people.license_plate = '94KL13X' AND month = 7 AND day = 28 AND year = 2021;--know accomplice
-- atm call less than a minute day 29 flight parking left in ten minuits
-- 94KL13X - 322W7JE