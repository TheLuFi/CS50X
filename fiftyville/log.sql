-- Keep a log of any SQL queries you execute as you solve the mystery.
.tables
 .schema crime_scene_reports

 SELECT * FROM crime_scene_reports WHERE street = 'Humphrey Street';

 .schema bakery_security_logs

 SELECT activity FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28;

 SELECT activity, license_plate, hour, minute FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10;

 .table

 SELECT id, name, transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

 .schema atm_transactions

 SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Humphrey Lane' AND transaction_type = 'withdraw';

 .table

 .schema phone_calls

 .schema flights

 SELECT * FROm flights WHERE year = 2023 AND month = 7 AND day = 29;

 .table

 .schema airports

 .table

 SELECT * FROM people AS p
 INNER JOIN bakery_security_logs AS b
 ON p.license_plate = b.license_plate
WHERE b.year = 2023 AND b.month = 7 AND b.day = 28 AND b.hour = 10;
--
--

SELECT name FROM people as p
JOIN passengers as pa
JOIN bakery_security_logs AS b
JOIN phone_calls AS ph
ON p.license_plate = b.license_plate AND p.passport_number = pa.passport_number
OR ph.caller = p.name AND ph.receiver = p.name
WHERE b.year = 2023 AND b.month = 7 AND b.day = 28 AND b.hour = 10 AND pa.flight_id = 36 GROUP BY p.name;

SELECT * FROM bakery_security_logs
   INNER JOIN people
   ON people.license_plate = bakery_security_logs.license_plate
   WHERE people.name = 'Bruce' OR people.name = 'Kesley' OR  people.name = 'Luca' OR people.name = 'Bruce'
   OR people.name = 'Sofia' OR people.name = 'Taylor';

   SELECT * FROM phone_calls as ph
   JOIN people as p
      ON ph.caller = p.phone_number
      WHERE p.name = 'Taylor'

SELECT a.amount, p.name FROM atm_transactions AS a
JOIN bank_accounts AS b
JOIN people AS p
   ON a.account_number = b.account_number AND b.person_id = p.id
   WHERE b.person_id IN (
      SELECT id FROM people WHERE people.name = 'Bruce' OR people.name = 'Kesley' OR people.name = 'Sofia'
   ) AND year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'


 SELECT p.name, at.atm_location, p.license_plate, bs.minute, pc.caller FROM passengers AS pa
   JOIN people AS p
   JOIN atm_transactions AS at
   JOIN bakery_security_logs AS bs
   JOIN phone_calls AS pc
   ON p.passport_number = pa.passport_number AND p.license_plate = bs.license_plate AND pc.caller = p.phone_number
   WHERE flight_id = 36 AND at.year = 2023 AND at.month = 7 AND at.day = 28 AND at.atm_location = 'Leggett Street' AND at.transaction_type = 'withdraw'
   AND bs.year = 2023 AND bs.month = 7 AND bs.day = 28 AND pc.year = 2023 AND pc.day = .month = 7 GR28 AND pcOUP BY p.name;

SELECT * FROM phone_calls AS pc
   JOIN people AS p
   ON p.phone_number = pc.caller
   WHERE p.name = 'Bruce' AND pc.year = 2023 AND pc.month = 7 AND pc.day = 28;

SELECT name FROM people WHERE phone_number = '(375) 555-8161';

