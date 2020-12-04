import java.io.File
import java.time.Year

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun isValid(passport: Map<String, String>): Boolean {
    return passport.containsKey("byr") && passport.containsKey("iyr") && passport.containsKey("eyr") &&
            passport.containsKey("hgt") && passport.containsKey("hcl") && passport.containsKey("ecl") &&
            passport.containsKey("pid")
}

fun parseInput(input: List<String>): List<Map<String, String>> {
    val passports: MutableList<Map<String, String>> = mutableListOf()
    var currentPassport: MutableMap<String, String> = mutableMapOf()
    for (line in input) {
        if (line == "") {
            // End of current passport
            passports.add(currentPassport)
            currentPassport = mutableMapOf()
        } else {
            // Parse line
            line.split(" ").forEach { element ->
                currentPassport[element.split(":")[0]] = element.split(":")[1]
            }
        }
    }
    return passports
}


fun main(args: Array<String>) {
    val passports = parseInput(getInput())
    val validPassports = passports.filter { predicate -> isValid(predicate) }
    println("First Solution:  ${validPassports.size}")
}