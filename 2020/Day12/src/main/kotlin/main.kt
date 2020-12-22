import java.io.File
import kotlin.math.*

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
    return Pair(x.roundToInt(),y.roundToInt())
}

fun executeCommand(
    input: String, currentShipPosition: Pair<Int, Int>, currentWayPointPosition: Pair<Int, Int>
): Pair<Pair<Int, Int>,Pair<Int, Int>> {
    // currentDirection is a unit vector
    val instruction = input[0]
    val magnitude = input.drop(1).toInt()
    var newWayPointPosition: Pair<Int, Int> = currentWayPointPosition
    var newShipPosition: Pair<Int, Int> = currentShipPosition
    when (instruction) {
        NORTH -> newWayPointPosition = Pair(currentWayPointPosition.first, currentWayPointPosition.second + magnitude)
        SOUTH -> newWayPointPosition = Pair(currentWayPointPosition.first, currentWayPointPosition.second - magnitude)
        EAST -> newWayPointPosition = Pair(currentWayPointPosition.first + magnitude, currentWayPointPosition.second)
        WEST -> newWayPointPosition = Pair(currentWayPointPosition.first - magnitude, currentWayPointPosition.second)
        TURN_LEFT -> newWayPointPosition = turn(currentWayPointPosition, magnitude)
        TURN_RIGHT -> newWayPointPosition = turn(currentWayPointPosition, 360-magnitude)
        FORWARD -> newShipPosition = Pair(
            currentShipPosition.first + currentWayPointPosition.first * magnitude,
            currentShipPosition.second + currentWayPointPosition.second * magnitude
        )
    }
    return Pair(newShipPosition, newWayPointPosition)
}

fun main(args: Array<String>) {
    val input = getInput("Input")

    var currentPosition = Pair(0,0)
    // East
    var currentDirection = Pair(10, 1)
//    println("Initial: Position (${currentPosition.first}, ${currentPosition.second}), Direction: ${currentDirection.first}, ${currentDirection.second})")
    for (command in input) {
        val output = executeCommand(command, currentPosition, currentDirection)
        currentPosition = output.first
        currentDirection = output.second
//        println("Input: $command, Position (${currentPosition.first}, ${currentPosition.second}), Direction: ${currentDirection.first}, ${currentDirection.second})")
    }
    val distance = getManhattanDistance(currentPosition, Pair(0,0))

    println("Second Solution: $distance")
}