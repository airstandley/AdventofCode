import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun convertInput(input: List<String>): List<Long> {
    val out: MutableList<Long> = mutableListOf()
    input.forEach { value -> out.add(value.toLong()) }
    return out
}

fun bruteForceInvalid(input: List<Long>, length: Int): Long {
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

fun bruteForceWeakness(input: List<Long>, key: Long): Long {
    // Find a continuous sequence that add to key
    var first: Int = 0
    var second: Int = 1
    var sequence: MutableList<Long> = mutableListOf()
    sequence.add(input[first])
    sequence.add(input[second])
    while (first < (input.size - 2) && second < (input.size - 1)) {
        val sum = sequence.reduce { acc, it -> acc + it }
        when {
            sum == key -> {
                // We've found the sequence
                sequence.sort()
                return sequence[0] + sequence.last()
            }
            sum > key -> {
                // Move the window floor
                first ++
                sequence = sequence.drop(1) as MutableList<Long>
            }
            else -> {
                // Move the window ceiling
                second ++
                sequence.add(input[second])
            }
        }
    }
    throw Exception("Invalid Code: Unable to find sequence.")
}

fun main(args: Array<String>) {
    val input = convertInput(getInput())
    val key = bruteForceInvalid(input, 25)
    println("First Solution: $key")
    val weakness = bruteForceWeakness(input, key)
    println("Second Solution $weakness")
}