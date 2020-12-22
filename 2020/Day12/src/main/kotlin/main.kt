import java.io.File
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.PI

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

fun turn(currentDirection: Pair<Int, Int>, angleInDegrees: Int): Pair<Int, Int> {
    val angleInRadians = angleInDegrees * PI/180
    val x = currentDirection.first * cos(angleInRadians) - currentDirection.second * sin(angleInRadians)
    val y = currentDirection.first * sin(angleInRadians) + currentDirection.second * cos(angleInRadians)
    return Pair(x.toInt(),y.toInt())
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
        TURN_LEFT -> newDirection = turn(currentDirection, magnitude)
        TURN_RIGHT -> newDirection = turn(currentDirection, 360-magnitude)
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