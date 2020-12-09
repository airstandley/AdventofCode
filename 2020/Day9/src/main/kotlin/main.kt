import sun.font.TrueTypeFont
import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun convertInput(input: List<String>): List<Long> {
    val out: MutableList<Long> = mutableListOf()
    input.forEach { value -> out.add(value.toLong()) }
    return out
}

fun bruteForce(input: List<Long>, length: Int): Long {
    for(test in length until input.size) {
        var match = false
        for (first in (test - length) until input.size) {
            for (second in (first + 1) until test) {
                if ((input[second] + input[first]) == input[test]) {
                    // test is valid, move on
                    match = true
                    break
                }
            }
            if (match) { break }
        }
        if (!match) {
            // We couldn't match this one
            return input[test]
        }
    }
    throw Exception("Invalid Code: All numbers in the sequence were valid")
}

fun main(args: Array<String>) {
    println("First Solution: ${bruteForce(convertInput(getInput()), 25)}")
}