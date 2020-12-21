import java.io.File

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

fun parseInput(input: List<String>): MutableList<MutableList<Char>> {
    val parsed = mutableListOf<MutableList<Char>>()
    for (line in input) {
        val parsedRow = mutableListOf<Char>()
        for (char in line) {
            parsedRow.add(char)
        }
        parsed.add(parsedRow)
    }
    return parsed
}

const val EMPTY_SEAT = 'L'
const val FLOOR = '.'
const val OCCUPIED_SEAT = '#'
const val OCCUPIED_SEAT_THRESHOLD = 5

fun getSurroundingSeatsFIRST(position: Pair<Int, Int>, seats: List<List<Char>>): List<Char> {
    val surroundingSeats = mutableListOf<Char>()
    for (i in position.first - 1 .. position.first + 1) {
        if (i < 0 || i > seats.lastIndex) { continue }
        for (j in position.second - 1 .. position.second + 1) {
            if (j < 0 || j > seats[i].lastIndex) { continue }
            if (i == position.first && j == position.second) { continue }
            surroundingSeats.add(seats[i][j])
        }
    }
    return surroundingSeats
}

fun getSurroundingSeats(position: Pair<Int, Int>, seats: List<List<Char>>): List<Char> {
    val surroundingSeats = mutableListOf<Char>()
    for (i in -1 .. 1) {
        for (j in -1 .. +1) {
            if (i == 0 && j == 0) { continue }
            // Check for the first seat on this vector
            var currentPosition = Pair(position.first, position.second)
            while(true) {
                // Update Position
                currentPosition = Pair(currentPosition.first + i, currentPosition.second + j)
                // Bounds checking
                if (currentPosition.first < 0 || currentPosition.first > seats.lastIndex) {
                    break
                }
                if (currentPosition.second < 0 || currentPosition.second > seats[currentPosition.first].lastIndex) {
                    break
                }
                // Seat Check
                if (seats[currentPosition.first][currentPosition.second] != FLOOR) {
                    surroundingSeats.add(seats[currentPosition.first][currentPosition.second])
                    break
                }
            }
        }
    }
    return surroundingSeats
}

fun updateEmptySeat(position: Pair<Int, Int>, seats: List<List<Char>>): Char {
    val occupiedSeats = getSurroundingSeats(position, seats).filter { seat -> seat == OCCUPIED_SEAT }
    if (occupiedSeats.isEmpty()) {
        // No adjacent seat is occupied. Seat becomes occupied
        return OCCUPIED_SEAT
    }
    return EMPTY_SEAT
}

fun updateOccupiedSeat(position: Pair<Int, Int>, seats: List<List<Char>>): Char {
    val occupiedSeats = getSurroundingSeats(position, seats).filter { seat -> seat == OCCUPIED_SEAT }
    if (occupiedSeats.size >= OCCUPIED_SEAT_THRESHOLD) {
        // 4 or more adjacent seats are occupied. Seat becomes empty
        return EMPTY_SEAT
    }
    return OCCUPIED_SEAT
}

fun getNextSeats(seats: List<List<Char>>): List<List<Char>> {
    val nextSeats: MutableList<MutableList<Char>> = mutableListOf()
    for (i in seats.indices) {
        nextSeats.add(mutableListOf())
        for (j in seats[i].indices) {
            when (seats[i][j]) {
                EMPTY_SEAT -> nextSeats[i].add(updateEmptySeat(Pair(i,j), seats))
                OCCUPIED_SEAT -> nextSeats[i].add(updateOccupiedSeat(Pair(i,j), seats))
                FLOOR -> nextSeats[i].add(FLOOR)
            }
        }
    }
    return nextSeats
}

fun isEqual(lastSeats: List<List<Char>>, nextSeats: List<List<Char>>): Boolean {
    for (i in lastSeats.indices) {
        for (j in lastSeats[i].indices) {
            if(lastSeats[i][j] != nextSeats[i][j]) {
                return false
            }
        }
    }
    return true
}

fun simulateSeating(initialSeats: List<List<Char>>): List<List<Char>> {
    var currentSeats = initialSeats
    var nextSeats = getNextSeats(currentSeats)
    while (!isEqual(currentSeats, nextSeats)) {
        currentSeats = nextSeats
        nextSeats = getNextSeats(currentSeats)
    }
    return currentSeats
}

fun getOccupiedSeatCount(seats: List<List<Char>>): Int {
    var count = 0
    for (row in seats) {
        val occupiedSeats = row.filter { seat -> seat == OCCUPIED_SEAT }
        count += occupiedSeats.size
    }
    return count
}

fun printSeats(seats: List<List<Char>>) {
    println("Seats:")
    for (line in seats) { println(line) }
    println("")
}

fun main(args: Array<String>) {
    val input = parseInput(getInput("Input"))
    val finalSeats = simulateSeating(input)
    val counts = getOccupiedSeatCount(finalSeats)
    println("Second Solution: $counts")
}