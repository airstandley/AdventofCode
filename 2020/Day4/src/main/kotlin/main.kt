import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun isAlphaNumeric(string: String): Boolean {
    for (char in string) {
        if (char !in 'A'..'Z'  && char !in 'a'..'z' && char !in '0'..'9') {
            return false
        }
    }
    return true
}

fun isValidLoose(passport: Map<String, String>): Boolean {
    return (
            passport.containsKey("byr") && passport.containsKey("iyr") && passport.containsKey("eyr") &&
            passport.containsKey("hgt") && passport.containsKey("hcl") && passport.containsKey("ecl") &&
            passport.containsKey("pid")
        )
}

fun isValidStrict(passport: Map<String, String>): Boolean {
    // validate byr
    val birthYear: Int? = passport["byr"]?.toIntOrNull()
    if (birthYear == null || birthYear > 2002 || birthYear < 1920) {
        return false
    }
    // validate iyr
    val issueYear: Int? = passport["iyr"]?.toIntOrNull()
    if (issueYear == null || issueYear > 2020 || issueYear < 2010) {
        return false
    }
    // validate eyr
    val expirationYear: Int? = passport["eyr"]?.toIntOrNull()
    if (expirationYear == null || expirationYear > 2030 || expirationYear < 2020) {
        return false
    }
    // validate hgt
    val unitOfMeasure: List<String> = listOf("cm", "in")
    val height: Pair<Int?, String?> = Pair(passport["hgt"]?.substring(0, (passport["hgt"]?.length?.minus(2)!!))?.toIntOrNull(), passport["hgt"]?.substring((passport["hgt"]?.length?.minus(2)!!), (passport["hgt"]?.length!!)))
    if (
        height.first == null || height.second == null || !unitOfMeasure.contains(height.second) ||
        (height.second == "cm" && (height.first!! > 193 || height.first!! < 150)) ||
        (height.second == "in" && (height.first!! > 76 || height.first!! < 59))
        ) {
            return false
    }
    // validate hcl
    val hcl: String? = passport["hcl"]
    if (
        hcl == null || hcl[0] != '#' ||
        hcl.subSequence(1, hcl.length).filter { char -> (char !in 'A'..'Z'  && char !in 'a'..'z' && char !in '0'..'9') }.any()
    ) {
        return false
    }
    // validate ecl
    val ecl: String? = passport["ecl"]
    val validEyeColors: List<String> = listOf("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    if (ecl !in validEyeColors) {
        return false
    }
    // validate pid
    val pid: String? = passport["pid"]
    if (pid == null || pid.filter { char -> (char in '0'..'9') }.length != 9) {
        return false
    }

    // VALID!
    return true
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
    val validPassportsLoose = passports.filter { predicate -> isValidLoose(predicate) }
    println("First Solution:  ${validPassportsLoose.size}")
    val validPassportsStrict = passports.filter { predicate -> isValidStrict(predicate)}
    println("Second Solution: ${validPassportsStrict.size}")
}