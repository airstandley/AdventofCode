import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

data class Command(val name: String, val function: (Int) -> Unit, val value: Int)

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
    return Command(command, function, value)
}

fun parseProgram(code: List<String>): List<Command> {
    val program: MutableList<Command> = mutableListOf()
    for (line in code) {
        program.add(parseCommand(line))
    }
    return program
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

fun run(program: List<Command>): Pair<Long, Boolean> {
    accumulator = 0
    programCounter = 0
    var infinite = false
    val infiniteLoopDetection: MutableMap<Int, List<Long>> = mutableMapOf()

    while (programCounter < program.size) {
        val command = program[programCounter]
        if (programCounter in infiniteLoopDetection) {
            // Since we don't jump based on accumulator yet, if we hit a command twice then we're infinite
            //println("Infinite Loop Detected at $programCounter")
            infinite = true
            break
        } else {
            infiniteLoopDetection[programCounter] = listOf(accumulator)
        }
        //println("$programCounter ${command.name} ${command.value} $accumulator")
        command.function(command.value)
    }
    return Pair(accumulator, infinite)
}

fun fixProgram(program: List<Command>): Pair<List<Command>, Long> {
    val fixedProgram: MutableList<Command> = mutableListOf(*program.toTypedArray())
    for(i in program.indices) {
        val command = program[i]
        when (command.name) {
            "acc" -> continue
            "nop" -> { fixedProgram[i] = Command("jmp", { v -> jump(v) }, command.value)}
            "jmp" -> { fixedProgram[i] = Command("nop", { v -> noop(v) }, command.value)}
        }
        val result = run(fixedProgram)
        if (!result.second) {
            //println("Fixed an infinite loop by changing $command to ${fixedProgram[i]}")
            return Pair(fixedProgram, result.first)
        } else {
            fixedProgram[i] = command
        }
    }
    throw Exception("Unable to Fix the Program!")
}

fun main(args: Array<String>) {
    val program = parseProgram(getInput())
    println("First Solution: ${run(program).first}")
    println("Second Solution: ${fixProgram(program).second}")
}