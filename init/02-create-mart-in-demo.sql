-- Витрина: агрегат по самолётам (фильтр: не отменённые рейсы)
\connect demo

SET search_path TO public, bookings;

DROP TABLE IF EXISTS public.airplanes_marts;

CREATE TABLE public.airplanes_marts AS
SELECT
  r.airplane_code,
  a.model,
  a.range,
  a.speed,
  COUNT(f.flight_id) AS flights_count
FROM flights f
JOIN routes r
  ON r.route_no = f.route_no
  AND r.validity @> f.scheduled_departure
JOIN airplanes a ON a.airplane_code = r.airplane_code
WHERE f.status <> 'Cancelled'
GROUP BY r.airplane_code, a.model, a.range, a.speed;

COMMENT ON TABLE public.airplanes_marts IS
  'Витрина pet-проекта: модель самолёта и число рейсов (без Cancelled)';
