open System

let countGoodTriplets (arr: int list) (a: int) (b: int) (c: int) =
    let isGoodTriplet i j k =
        abs (arr.[i] - arr.[j]) <= a &&
        abs (arr.[j] - arr.[k]) <= b &&
        abs (arr.[i] - arr.[k]) <= c

    let rec countTriplets i j k count =
        match i, j, k with
        | _, _, _ when i >= List.length arr - 2 -> count
        | _, _, _ when j >= List.length arr - 1 -> countTriplets (i + 1) (i + 2) (i + 3) count
        | _, _, _ when k >= List.length arr -> countTriplets i (j + 1) (j + 2) count
        | _, _, _ ->
            let newCount = if isGoodTriplet i j k then count + 1 else count
            countTriplets i j (k + 1) newCount

    countTriplets 0 1 2 0
let check () =
    if countGoodTriplets [3; 0; 1; 1; 9; 7] 7 2 3 <> 0 then
        failwith "Test Case 1 failed"
    if countGoodTriplets [1; 1; 2; 2; 3] 0 0 1 <> 0 then
        failwith "Test Case 2 failed"
    if countGoodTriplets [1; 2; 3; 4; 5] 1 1 1 <> 0 then
        failwith "Test Case 3 failed"

check ()