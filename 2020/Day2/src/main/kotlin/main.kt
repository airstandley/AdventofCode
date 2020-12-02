import java.io.File

data class PasswordPolicy(val char: Char, val min: Int = 0, val max: Int = 0)

fun getInput(): List<String> {
    return File("Input").readLines()
}

private val linRegex = Regex("(\\d*)-(\\d*) (\\w): (\\w*)")
fun parseInputLine(line: String): Pair<PasswordPolicy, String>? {
    // Input is formatted "min-max char: password"
    val match = linRegex.find(line)
    if (match != null) {
        val values: List<String> = match.groupValues
        return Pair(
            PasswordPolicy(values[3][0], values[1].toInt(), values[2].toInt()),
            values[4]
        )
    }
    return null
}

fun countCharOccurrence(password: String, char: Char): Int {
    // Count how many times char appears in password
    var count = 0
    password.forEach { passChar -> if (passChar == char) { count ++ } }
    return count
}

fun isPasswordValid(policy: PasswordPolicy, password: String): Boolean {
    val count = countCharOccurrence(password, policy.char)
    return policy.min <= count && count <= policy.max
}

fun countValidPasswords(lines: List<String>): Int {
    var count = 0
    for (line in lines) {
        val (policy, password) = parseInputLine(line) ?: continue
        if (isPasswordValid(policy, password)) { count++ }
    }
    return count
}

fun main(args: Array<String>) {
    println("First Solution ${countValidPasswords(getInput())}")
}