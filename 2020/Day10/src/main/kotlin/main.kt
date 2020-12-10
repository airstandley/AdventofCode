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

fun main(args: Array<String>) {
    val input = parseInput(getInput("Input")) as MutableList<Int>
    input.sort()
    input.add(input.last() + 3)
    var oneVolt = 0
    var twoVolt = 0
    var threeVolt = 0
    var last = 0
    for (i in input) {
        when (i - last) {
            1 -> {oneVolt++ }
            2 -> {twoVolt++ }
            3 -> {threeVolt++ }
            else -> { throw Exception("Invalid List. Can't go from $last to $i")}
        }
        last = i
    }
    println("One Volt: $oneVolt, Two Volt: $twoVolt, Three Volt: $threeVolt")
    println("First Solution: ${oneVolt * threeVolt}")
}