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

fun applyAddressMask(bitmask: String, value: Long): String {
    val addressString = convertToBitString(value.toLong())
    var maskedString = ""
    for (i in bitmask.indices) {
        when(bitmask[i]) {
            'X' -> maskedString += 'X'
            '1' -> maskedString += '1'
            '0' -> maskedString += addressString[i]
        }
    }
    return maskedString
}

var BITMASK: String = ""
val MEMORY: MutableMap<Long, Long> = mutableMapOf()

fun store(address: Long, value: Long){
    MEMORY[address] = value
}

fun storeFluctuating(address: String, value: Long, index: Int = 0) {
    for (i in index until address.length) {
        if (address[i] == 'X') {
            val address1 = address.replaceFirst('X', '1')
            val address0 = address.replaceFirst('X', '0')
            storeFluctuating(address0, value, i)
            storeFluctuating(address1, value, i)
            return
        }
    }
    // There are no fluctuating bits in this string
    val finalAddress = convertToLong(address).toLong()
    store(finalAddress, value)
}

fun sumMemory(): Long {
    var sum: Long = 0
    MEMORY.forEach { (key, value) -> sum += value}
    return sum
}

fun executeCommandV1(command: String) {
    val parts = command.split(" = ")
    if (parts[0] == "mask") {
        BITMASK = parts[1]
    } else {
        val address = parts[0].drop(4).split("]")[0].toLong()
        store(address, applyBitmask(BITMASK, parts[1].toLong()))
    }
}

fun executeCommandV2(command: String) {
    val parts = command.split(" = ")
    if (parts[0] == "mask") {
        BITMASK = parts[1]
    } else {
        val address = parts[0].drop(4).split("]")[0].toLong()
        storeFluctuating(applyAddressMask(BITMASK, address), parts[1].toLong())
    }
}

fun run(program: List<String>, version: String): Long{
    // Initialize MEMORY and MASK
    MEMORY.forEach { (key, _) -> MEMORY[key] = 0}
    BITMASK = ""
    for (command in program) {
        when(version) {
            "1" -> executeCommandV1(command)
            "2" -> executeCommandV2(command)
        }
    }
    return sumMemory()
}

fun main(args: Array<String>) {
    val input = getInput("Input")
    val sum1 = run(input, "1")
    println("First Solution: $sum1")
    val sum2 = run(input, "2")
    println("Second Solution: $sum2")
}