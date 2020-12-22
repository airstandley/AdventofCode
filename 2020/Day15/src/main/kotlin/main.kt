import java.io.File

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

fun getStartingNumbers(input: List<String>): List<Int> {
    val numbers = mutableListOf<Int>()
    input[0].split(",").forEach { item -> numbers.add(item.toInt())  }
    return numbers
}

fun playGame(startingNumbers: List<Int>, turnLimit: Int): Int {
    var lastNumber = startingNumbers.first()
    val spokenMap = mutableMapOf<Int, Int>()
    var i = 0
    for (j in startingNumbers.indices) {
        i = j
        val number = startingNumbers[j]
        spokenMap[lastNumber] = i
        lastNumber = number
    }
    while (i < (turnLimit - 1)) {
        i++
        val number = if (lastNumber in spokenMap) { i - spokenMap[lastNumber] as Int } else { 0 }
        spokenMap[lastNumber] = i
        lastNumber = number
    }
    return lastNumber
}

fun main(args: Array<String>) {
    val last1 = playGame(getStartingNumbers(getInput("Input")), 2020)
    println("First Solution: $last1")
    val last2 = playGame(getStartingNumbers(getInput("Input")), 30000000)
    println("Second Solution: $last2")
}