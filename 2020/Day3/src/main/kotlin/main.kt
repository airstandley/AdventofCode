import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

val TREE = '#'
val GROUND = '.'

class Slope(val grid: List<String>, start: Pair<Int, Int>) {
    var x = start.first
    var y = start.second

    fun position(): Char {
        return this.grid[this.y][this.x]
    }

    fun atBottom(): Boolean {
        return this.y == (this.grid.size - 1)
    }

    fun moveDownSlope(angle: Pair<Int, Int>): Char {
        val (x, y) = angle
        this.y += y
        this.x += x
        if (this.x >= this.grid[this.y].length) {
            this.x = this.x - this.grid[this.y].length
        }
        return this.position()
    }
}

fun countTreesInPath(slope: Slope, angle: Pair<Int, Int>): Int {
    var count = 0
    while (!slope.atBottom()) {
        if (slope.moveDownSlope(angle) == TREE) {
            count ++
        }
    }
    return count
}

val anglesToCheck = listOf(Pair(1,1), Pair(3,1), Pair(5,1), Pair(7,1), Pair(1,2))

fun main(args: Array<String>) {
    println("First Solution: ${countTreesInPath(Slope(getInput(), Pair(0,0)), Pair(3,1))}")
    val counts = ArrayList<Int>(anglesToCheck.size)
    anglesToCheck.forEach { angle -> counts.add(countTreesInPath(Slope(getInput(), Pair(0,0)), angle)) }
    println("Counts: ${counts}")
    var sum: Double = 1.0
    counts.forEach {count -> sum = sum * count}
    println("Second Solution: ${sum.toBigDecimal().toPlainString()}")
}