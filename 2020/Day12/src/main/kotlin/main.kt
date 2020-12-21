import java.io.File
import kotlin.math.abs

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

const val NORTH = 'N'
const val SOUTH = 'S'
const val EAST = 'E'
const val WEST = 'W'
const val TURN_LEFT = 'L'
const val TURN_RIGHT = 'R'
const val FORWARD = 'F'

fun getManhattanDistance(endPosition: Pair<Int, Int>, startPosition: Pair<Int, Int> = Pair(0,0)): Int {
    val x = endPosition.first - startPosition.first
    val y = endPosition.second - startPosition.second
    return abs(x) + abs(y)
}

fun turn90(currentDirection: Pair<Int, Int>): Pair<Int, Int> {
    val x: Int
    val y: Int
    when(currentDirection.first) {
        1, -1 -> x = 0
        0 -> x = if(currentDirection.second > 0) { 1 } else { -1 }
        else -> throw Exception("Invalid Int vector")
    }
    when(currentDirection.second) {
        1, -1 -> y = 0
        0 -> y = if(currentDirection.first > 0) { -1 } else { 1 }
        else -> throw Exception("Invalid Int vector")
    }
    return Pair(x,y)
}

fun turn(currentDirection: Pair<Int, Int>, magnitude: Int): Pair<Int, Int> {
    when(magnitude) {
        90 -> return turn90(currentDirection)
        180 -> return turn90(turn90(currentDirection))
        270 -> return turn90(turn90(turn90(currentDirection)))
        else -> throw Exception("Invalid Turn Mag: $magnitude")
    }
}

fun executeCommand(
    input: String, currentPosition: Pair<Int, Int>, currentDirection: Pair<Int, Int>
): Pair<Pair<Int, Int>,Pair<Int, Int>> {
    // currentDirection is a unit vector
    val instruction = input[0]
    val magnitude = input.drop(1).toInt()
    var newDirection: Pair<Int, Int> = currentDirection
    var newPosition: Pair<Int, Int> = currentPosition
    when (instruction) {
        NORTH -> newPosition = Pair(currentPosition.first, currentPosition.second + magnitude)
        SOUTH -> newPosition = Pair(currentPosition.first, currentPosition.second - magnitude)
        EAST -> newPosition = Pair(currentPosition.first + magnitude, currentPosition.second)
        WEST -> newPosition = Pair(currentPosition.first - magnitude, currentPosition.second)
        TURN_LEFT -> newDirection = turn(currentDirection, 360-magnitude)
        TURN_RIGHT -> newDirection = turn(currentDirection, magnitude)
        FORWARD -> newPosition = Pair(
            currentPosition.first + currentDirection.first * magnitude,
            currentPosition.second + currentDirection.second * magnitude
        )
    }
    return Pair(newPosition, newDirection)
}

fun main(args: Array<String>) {
    val input = getInput("Input")

    var currentPosition = Pair(0,0)
    // East
    var currentDirection = Pair(1, 0)
//    println("Initial: Position (${currentPosition.first}, ${currentPosition.second}), Direction: ${currentDirection.first}, ${currentDirection.second})")
    for (command in input) {
        val output = executeCommand(command, currentPosition, currentDirection)
        currentPosition = output.first
        currentDirection = output.second
//        println("Input: $command, Position (${currentPosition.first}, ${currentPosition.second}), Direction: ${currentDirection.first}, ${currentDirection.second})")
    }
    val distance = getManhattanDistance(currentPosition, Pair(0,0))

    println("First Solution: $distance")
}