from(bucket: "data-test-1")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) =>
    r._measurement == "noiselevel" and
    r.classroom == "211" and
    r._field == "valor"
  )
  |> keep(columns: ["_time", "_value", "classroom"])
  |> rename(columns: {_time: "time", _value: "valor"})