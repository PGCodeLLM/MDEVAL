open System

let sortByBinaryOnes (arr: int list) =
    
    let countBinaryOnes (n:int) =
        Convert.ToString(n, 2) |> Seq.filter (fun x -> x = '1') |> Seq.length

    arr |> List.sortWith (fun x y -> 
        let onesX, onesY = countBinaryOnes x, countBinaryOnes y
        if onesX = onesY then compare x y
        else compare onesX onesY)

let check () =
    if sortByBinaryOnes [0; 1; 2; 3; 4; 5; 6; 7; 8] <> [0; 1; 2; 4; 8; 3; 5; 6; 7] then
        failwith "Test Case 1 failed"
    if sortByBinaryOnes [1024; 512; 256; 128; 64; 32; 16; 8; 4; 2; 1] <> [1; 2; 4; 8; 16; 32; 64; 128; 256; 512; 1024] then
        failwith "Test Case 2 failed"
    if sortByBinaryOnes [10; 100; 1000; 10000] <> [10; 100; 10000; 1000] then
        failwith "Test Case 3 failed"
    if sortByBinaryOnes [3; 7; 15; 31; 63] <> [3; 7; 15; 31; 63] then
        failwith "Test Case 4 failed"
    if sortByBinaryOnes [5; 9; 17; 33; 65] <> [5;9;17; 33; 65;] then
        failwith "Test Case 5 failed"

check ()