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

fun buildSeatMap(rows: Int, columns: Int): MutableMap<Int, MutableMap<Int, Boolean>> {
    // Build a seat hash map
    val r = rows - 1
    val c = columns - 1
    val seatMap = mutableMapOf<Int, MutableMap<Int, Boolean>>()
    for (row in 0..r) {
        val columnMap = mutableMapOf<Int, Boolean>()
        for (column in 0..c) {
            columnMap[column] = true
        }
        seatMap[row] = columnMap
    }
    return seatMap
}

fun removeSeat(seatLocation: Pair<Int, Int>, seatMap: MutableMap<Int, MutableMap<Int, Boolean>>) {
    seatMap[seatLocation.first]?.set(seatLocation.second, false)
}

fun findMySeat(seatMap: MutableMap<Int, MutableMap<Int, Boolean>>): Pair<Int, Int>? {
    var lastRowEmpty = true
    var potentialLocation: Pair<Int, Int>? = null
    for (row in seatMap.keys) {
        val columnMap = seatMap[row]
        var emptyRow = false
        var potentialColumn: Int? = null
        if (columnMap != null) {
            for (column in columnMap.keys) {
                if (columnMap[column] == true){
                    // Found an empty seat
                    if (potentialColumn == null) {
                        // This might be it!
                        potentialColumn = column
                    } else {
                        // Two empty columns on this row, this can't be it
                        emptyRow = true
                        break
                    }
                }
            }
        }
        if (emptyRow) {
            if (potentialLocation != null) {
                // Can't be the seat if it's next to an empty row
                potentialLocation = null
            }
            lastRowEmpty = true
        } else if (potentialColumn != null) {
            if (!lastRowEmpty) {
                potentialLocation = Pair(row, potentialColumn)
            }
            lastRowEmpty = true
        } else {
            if (potentialLocation != null) {
                // We found a location with full rows on either side. This should be it
                return potentialLocation
            }
            lastRowEmpty = false
        }
    }
    return null
}

fun printSeatMap(seatMap: MutableMap<Int, MutableMap<Int, Boolean>>) {
    for (entry in seatMap) {
        var rowString = "${entry.key}: "
        for (column in entry.value) {
            if (column.value) {
                rowString += "="
            } else {
                rowString += "X"
            }
        }
        println(rowString)
    }
}

fun main(args: Array<String>) {
    var maxSeatId = 0
    val seatMap = buildSeatMap(ROWS, COLUMNS)
    for (locationString in getInput()) {
        val seatLocation = findSeat(locationString)
        val seatId = getSeatId(seatLocation)
        if (seatId > maxSeatId) { maxSeatId = seatId }
        //println("String: $locationString, Location: (${seatLocation.first}, ${seatLocation.second}), ID: $seatId")
        removeSeat(seatLocation, seatMap)
    }
    println("First Solution: $maxSeatId")
    val mySeatLocation = findMySeat(seatMap)
    //printSeatMap(seatMap)
    if (mySeatLocation != null ) {
        println("Second Solution: ${getSeatId(mySeatLocation)}")
    } else {
        throw Exception("COULD NOT FIND MY SEAT!")
    }
}