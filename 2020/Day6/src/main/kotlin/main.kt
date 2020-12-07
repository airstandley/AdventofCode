import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun getGroups(input: List<String>): MutableList<MutableList<String>> {
    val groups = mutableListOf<MutableList<String>>()
    var currentGroup = mutableListOf<String>()
    for (line in input) {
        if (line == "") {
            // End of current group
            groups.add(currentGroup)
            currentGroup = mutableListOf()
        } else {
            //Add to current group
            currentGroup.add(line)
        }
    }
    groups.add(currentGroup)
    return groups
}

fun getYesQuestionsForGroup1(group: List<String>): MutableSet<Char> {
    // Get any char to which ANYONE in the group gave
    val yesQuestions: MutableSet<Char> = mutableSetOf()
    for (answers in group) {
        for (char in answers) {
            yesQuestions.add(char)
        }
    }
    return yesQuestions
}

fun getYesQuestionsForGroup2(group: List<String>): MutableSet<Char> {
    // Get only char that EVERYONE in the group gave
    var groupYesQuestions:MutableSet<Char> = mutableSetOf()
    var first = true
    for (answers in group) {
        val personYesQuestions = mutableSetOf<Char>()
        for (char in answers) {
            personYesQuestions.add(char)
        }
        if (first) {
            // First response
            groupYesQuestions = personYesQuestions
            first = false
        } else {
            groupYesQuestions = groupYesQuestions.intersect(personYesQuestions) as MutableSet<Char>
        }
    }
    return groupYesQuestions
}

fun main(args: Array<String>) {
    val groups = getGroups(getInput())
    var sum1 = 0
    var sum2 = 0
    for (group in groups) {
        val yesQuestions1 = getYesQuestionsForGroup1(group)
        //println("${yesQuestions1.size}: $yesQuestions1")
        val yesQuestions2 = getYesQuestionsForGroup2(group)
        //println("${yesQuestions2.size}: $yesQuestions2")
        sum1 += yesQuestions1.size
        sum2 += yesQuestions2.size
    }
    println("First Solution: $sum1")
    println("Second Solution: $sum2")
}