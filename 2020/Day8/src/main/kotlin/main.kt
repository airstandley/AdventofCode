import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

data class Command(val function: (Int) -> Unit, val value: Int)

fun parseCommand(input:String): Command {
    val parts = input.split(" ")
    val command = parts[0]
    val sign = parts[1].drop(1)
    val value = if (sign ==  "-") { parts[1].toInt() * -1 } else { parts[1].toInt() }
    val function: (Int) -> Unit = when (command) {
        "acc" -> {
            { v -> accumulate(v) }
        }
        "jmp" -> {
            { v -> jump(v) }
        }
        "nop" -> {
            { v -> noop(v) }
        }
        else -> {
            { v ->  invalid(v, command) }
        }
    }
    return Command(function, value)
}

var accumulator: Long = 0
var programCounter: Int = 0

fun accumulate(value: Int) {
    // Increment or De-increment the global accumulator
    accumulator += value
    programCounter++
}

fun jump(offset: Int) {
    // Jump by offset
    programCounter += offset
}

fun noop(value: Int) {
    // Do Nothing
    programCounter++
}

fun invalid(value: Int, command:String) {
    throw Exception("Invalid Command $command $value")
}

fun main(args: Array<String>) {
    accumulator = 0
    programCounter = 0
    val program = getInput()

    val infiniteLoopDetection: MutableMap<Int, List<Long>> = mutableMapOf()

    while (programCounter < program.size) {
        val input = program[programCounter]
        val command = parseCommand(input)
        if (programCounter in infiniteLoopDetection) {
            // Since we don't jump based on accumulator yet, if we hit a command twice then we're infinite
            println("Infinite Loop Detected at $programCounter")
            break
        } else {
            infiniteLoopDetection[programCounter] = listOf(accumulator)
        }
        println("$programCounter $input $command")
        command.function(command.value)
    }

    println("First Solution: $accumulator")
}