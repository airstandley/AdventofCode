import java.io.File

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

fun parseInput(input: List<String>): Pair<Int, List<Int>> {
    assert(input.size == 2)
    val timestamp: Int = input[0].toInt()
    val busIds = mutableListOf<Int>()
    val ids: List<String> = input[1].split(',')
    for (id in ids) {
        if(id == "x") {
            continue
        }
        busIds.add(id.toInt())
    }
    return Pair(timestamp, busIds)
}

fun getNextBus(initialTimestamp: Int, ids: List<Int>): Pair<Int, Int> {
    // Return the Bus and Timestamp for the next available bus.
    var timestamp = initialTimestamp
    // If a bus doesn't depart by twice the initial then it probably never will.
    while (timestamp < initialTimestamp * 2) {
        val departingBuses = ids.filter { id -> (timestamp.rem(id) == 0) }
        if (!departingBuses.isEmpty()) {
            // Return the first match since the problem is set up in such
            // a wat that it's assume no id is a multiple of another id.
            return Pair(timestamp, departingBuses.first())
        }
        timestamp++
    }
    throw Exception("No departing bus found!")
}

fun main(args: Array<String>) {
    val input = parseInput(getInput("Input"))
    val timestamp = input.first
    val ids = input.second
    val output = getNextBus(timestamp, ids)
    val departing = output.first
    val bus = output.second
    val solutionOne = (departing - timestamp) * bus
    println("First Solution: $solutionOne")
}