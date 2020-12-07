import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}


const val ROWS = 128
const val COLUMNS = 8

fun findSeat(seatLocation: String): Pair<Int, Int> {
    // Bucket Range (Min, Max) and Bucket Size (128)
    var row = Triple(0, ROWS - 1, ROWS)
    var column = Triple(0, COLUMNS - 1, COLUMNS)

    for (char in seatLocation) {
        when (char) {
            'F' -> {
                // Lower half of the row bucket
                val newBucketSize = row.third / 2
                val newMax = row.second - newBucketSize
                row = Triple(row.first, newMax, newBucketSize)
            }
            'B' -> {
                // Upper half of the row bucket
                val newBucketSize = row.third / 2
                val newMin = row.first + newBucketSize
                row = Triple(newMin, row.second, newBucketSize)
            }
            'L' -> {
                // Lower half of the column bucket
                val newBucketSize = column.third / 2
                val newMax = column.second - newBucketSize
                column = Triple(column.first, newMax, newBucketSize)
            }
            'R' -> {
                // Upper half of the row bucket
                val newBucketSize = column.third / 2
                val newMin = column.first + newBucketSize
                column = Triple(newMin, column.second, newBucketSize)
            }
            else -> throw Exception("Invalid seat location string: $seatLocation")
        }
    }
    return Pair(row.first, column.first)
}

fun getSeatId(location: Pair<Int,Int>): Int {
    // Seat Id is row * 8 + column
    return location.first * 8 + location.second
}

fun main(args: Array<String>) {
    var maxSeatId = 0
    for (locationString in getInput()) {
        val seatLocation = findSeat(locationString)
        val seatId = getSeatId(seatLocation)
        if (seatId > maxSeatId) { maxSeatId = seatId }
        //println("String: $locationString, Location: (${seatLocation.first}, ${seatLocation.second}), ID: $seatId")
    }
    println("First Solution: $maxSeatId")
}