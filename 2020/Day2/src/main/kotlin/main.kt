import java.io.File

data class PasswordPolicy(val char: Char, val first: Int = 0, val second: Int = 0)

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

fun isPasswordValidFirst(policy: PasswordPolicy, password: String): Boolean {
    // Password contains at least first occurrences of char and not more than second
    val count = countCharOccurrence(password, policy.char)
    return policy.first <= count && count <= policy.second
}

fun isPasswordValidSecond(policy: PasswordPolicy, password: String): Boolean {
    // Password contains char at first or second position, but not at both
    val first = password[policy.first - 1] == policy.char
    val second = password[policy.second - 1] == policy.char
    return ((first && !second) || (second && !first))
}

fun countValidPasswords(lines: List<String>, validationMethod: (PasswordPolicy, String) -> Boolean): Int {
    var count = 0
    for (line in lines) {
        val (policy, password) = parseInputLine(line) ?: continue
        if (validationMethod(policy, password)) { count++ }
    }
    return count
}

fun main(args: Array<String>) {
    val firstValidationMethod: (PasswordPolicy, String) -> Boolean = {
        policy, password -> isPasswordValidFirst(policy, password)
    }
    println("First Solution: ${countValidPasswords(getInput(), firstValidationMethod)}")
    val secondValidationMethod: (PasswordPolicy, String) -> Boolean = {
        policy, password -> isPasswordValidSecond(policy, password)
    }
    println("Second Solution: ${countValidPasswords(getInput(), secondValidationMethod)}")
}