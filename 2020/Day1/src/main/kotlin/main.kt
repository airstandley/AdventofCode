import java.io.File
import java.util.*

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun parseExpenseReport(lineItems: List<String>, sum: Int): Pair<Int, Int>? {
    // Parse the expense report to find the first two number that sum to the given sum.
    // For now brute-force and iterate over the list for ever item in the list
    for (i in lineItems.indices) {
        val first = lineItems[i].toIntOrNull() ?: continue
        for (j in (i+1) until lineItems.size) {
            val second = lineItems[j].toIntOrNull() ?: continue
            if ((first + second) == sum) {
                return Pair(first, second)
            }
        }
    }
    return null
}

fun main(args: Array<String>) {
    val pair = parseExpenseReport(getInput(), 2020)
    if (pair != null) {
        val (first, second) = pair
        println("Solution: ${first * second}")
    }
}