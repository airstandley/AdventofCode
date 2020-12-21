import java.io.File


fun getInput(file: String): List<String> {
    return File(file).readLines()
}

fun parseInput(input: List<String>): List<Int> {
    val output: MutableList<Int> = mutableListOf()
    for (line in input) {
        output.add(line.toInt())
    }
    return output
}

fun countAdapterGaps(adapters: List<Int>): Triple<Int, Int, Int> {
    var oneVolt = 0
    var twoVolt = 0
    var threeVolt = 0
    for (i in 1 until adapters.size) {
        when (adapters[i] - adapters[i - 1]) {
            1 -> {
                oneVolt++
            }
            2 -> {
                twoVolt++
            }
            3 -> {
                threeVolt++
            }
            else -> {
                throw Exception("Invalid List. Can't go from ${adapters[i - 1]} to ${adapters[i]}")
            }
        }
    }
    return Triple(oneVolt, twoVolt, threeVolt)
}

val countViableArrangementCalls: MutableMap<List<Int>, Long> = mutableMapOf()

fun countViableArrangements(adapters: List<Int>): Long {
    var arrangements: Long = 0
    for (i in 1 until adapters.size - 1) {
        println("(${adapters.first()} - ${adapters.last()}) Index: $i, Item: ${adapters[i]}, Count: $arrangements")
        // See if we can drop this element
        if (adapters[i + 1] - adapters[i - 1] <= 3) {
            // Include all the valid paths with this element removed
            val newList: MutableList<Int> = adapters.slice(IntRange(i + 1, adapters.size - 1)) as MutableList<Int>
            newList.add(0, adapters[i - 1])
            println("Dropping ${adapters[i]}, NewList: ${newList.first()} to ${newList.last()}")
            arrangements += countViableArrangementCalls.getOrPut(newList) { countViableArrangements(newList) }
        }
    }
    return arrangements + 1
}

fun main(args: Array<String>) {
    val input = parseInput(getInput("Input")) as MutableList<Int>
    input.sort()
    input.add(0, 0)
    input.add(input.last() + 3)
    val counts = countAdapterGaps(input)
    println("On Volt: ${counts.first}, Two Volts: ${counts.second}, Three Volts: ${counts.third}")
    println("First Solution: ${counts.first*counts.second}")
    val permutations = countViableArrangements(input)
    println("Second Solution: ${permutations.toBigDecimal().toPlainString()}")
}