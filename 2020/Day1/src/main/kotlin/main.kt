import java.io.File
import java.util.*

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun parseExpenseReport(lineItems: List<String>, sum: Int): Pair<Pair<Int, Int>?, Triple<Int,Int,Int>?> {
    // Parse the expense report to find the first two number that sum to the given sum.
    // For now brute-force and iterate over the list for ever item in the list
    var pair: Pair<Int, Int>? = null
    var triple: Triple<Int, Int, Int>? = null
    for (i in lineItems.indices) {
        val first = lineItems[i].toIntOrNull() ?: continue
        for (j in (i+1) until lineItems.size) {
            val second = lineItems[j].toIntOrNull() ?: continue
            if (triple ==  null) {
                for (k in (j + 1) until lineItems.size) {
                    val third = lineItems[k].toIntOrNull() ?: continue
                    if ((first + second + third) == sum) {
                        triple = Triple(first, second, third)
                        break
                    }
                }
            }
            if (pair == null && (first + second) == sum) {
                pair = Pair(first, second)
            }
            if (pair != null && triple != null) { break }  // Short if we've found them
        }
        if (pair != null && triple != null) { break }  // Short if we've found them
    }
    return Pair(pair, triple)
}

fun main(args: Array<String>) {
    val (pair, triple) = parseExpenseReport(getInput(), 2020)
    if (pair != null) {
        val (first, second) = pair
        println("First Solution: ${first * second}")
    }
    if (triple != null) {
        val (first, second, third) = triple
        println("Second Solution: ${first * second * third}")
    }
}