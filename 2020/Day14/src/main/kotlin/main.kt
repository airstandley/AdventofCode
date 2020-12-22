import java.io.File
import kotlin.math.pow

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

fun convertToBitString(value: Long): String {
    var string = ""
    var rem = value
    for (i in 35 downTo 0) {
        if(rem == 0.toLong()) {
            string += "0"
            continue
        }
        val bitValue = 2.toDouble().pow(i).toInt()
        if (bitValue <= rem) {
            // 1
            string += "1"
            rem -= bitValue
        } else {
            // 0
            string += "0"
        }
    }
    return string
}

fun convertToLong(bitString: String): Long {
    assert(bitString.length == 36)
    var i = 35
    var value: Long = 0
    for (bit in bitString) {
        if (bit == '1') {
            val bitValue = 2.toDouble().pow(i).toLong()
            value += bitValue
        }
        i--
    }
    return value
}

fun applyBitmask(bitmask: String, value: Long): Long {
    val bitString = convertToBitString(value)
    var maskedString = ""
    for (i in bitmask.indices) {
        when(bitmask[i]) {
            'X' -> maskedString += bitString[i]
            '1' -> maskedString += '1'
            '0' -> maskedString += '0'
        }
    }
    return convertToLong(maskedString)
}

var BITMASK: String = ""
val MEMORY: MutableMap<Int, Long> = mutableMapOf()

fun store(address: Int, value: Long){
    MEMORY[address] = value
}

fun sumMemory(): Long {
    var sum: Long = 0
    MEMORY.forEach { (key, value) -> sum += value}
    return sum
}

fun executeCommand(command: String) {
    val parts = command.split(" = ")
    if (parts[0] == "mask") {
        BITMASK = parts[1]
    } else {
        val address = parts[0].drop(4).split("]")[0].toInt()
        store(address, applyBitmask(BITMASK, parts[1].toLong()))
    }
}

fun run(program: List<String>): Long{
    for (command in program) {
        executeCommand(command)
    }
    return sumMemory()
}

fun main(args: Array<String>) {
    val input = getInput("Input")
    val sum = run(input)
    println("First Solution: $sum")
}