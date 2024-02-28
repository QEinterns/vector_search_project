import logging
def multiline_to_single_conv(text, debug_mode = 0):

    new_text  = text.replace('"', "'") #to remove double quotes
    new_text  = new_text.replace('\n','') #to remove new lines

    if(debug_mode):
        print("The plot is : \n")
        print(new_text)
        print("\n")
     
    return new_text


#sample call
# multiline_to_single_conv("""More than 30 years after graduating from Top Gun,[a] United States Navy Captain Pete "Maverick" Mitchell is a decorated test pilot whose repeated insubordination has kept him from flag rank.[b] When Rear Admiral Chester "Hammer" Cain plans to cancel the hypersonic "Darkstar" scramjet program Maverick is testing on the grounds that it has not reached the contract specification of Mach 10, Maverick unilaterally changes the target speed for that day's test from Mach 9 to Mach 10 and commences the test early in order to prove Cain wrong. During the test flight, Maverick successfully reaches Mach 10 in the Darkstar prototype; however, the prototype aircraft is destroyed when Maverick cannot resist pushing his airspeed beyond Mach 10.

# After the flight, Cain tells Maverick that he would be grounded if not for Admiral Tom "Iceman" Kazansky, Maverick's friend and former Top Gun rival. Iceman, now commander of the U.S. Pacific Fleet, has assigned Maverick to the Top Gun school at NAS North Island.

# The Navy has been ordered to destroy an unsanctioned uranium enrichment plant before it becomes operational. The plant, located in an underground bunker at the end of a canyon, is defended by surface-to-air missiles (SAMs), GPS jammers, and fifth-generation Su-57 fighters as well as older F-14 Tomcats. Maverick devises a plan employing two pairs of F/A-18E/F Super Hornets armed with laser-guided bombs, but instead of participating in the strike, he is to train an elite group of Top Gun graduates assembled by Air Boss Vice Admiral Beau "Cyclone" Simpson.

# Maverick dogfights his skeptical students and prevails in every contest, winning their respect. Two of the students clash: Lieutenants Jake "Hangman" Seresin and Bradley "Rooster" Bradshaw—son of Maverick's deceased best friend and RIO Nick "Goose" Bradshaw. Rooster dislikes Hangman's cavalier attitude, while Hangman criticizes Rooster's cautious flying. Maverick reunites with former girlfriend Penny Benjamin, to whom he reveals that he promised Rooster's dying mother that Rooster would not become a pilot. Rooster, unaware of the promise, angrily resents Maverick for blocking his Naval Academy application—impeding his military career—and blames him for his father's death. Maverick is reluctant to further interfere with Rooster's career, but the alternative is to send him on the extremely dangerous mission. He tells his doubts to Iceman, who has terminal throat cancer. Iceman tells him, "It's time to let go" and reassures him that both the Navy and Rooster need Maverick.

# Iceman dies soon after, and after an F/A-18F crashes during training, Cyclone removes Maverick as instructor. He relaxes the mission parameters so they are easier to execute but make escape much more difficult. During Cyclone's announcement, Maverick makes an unauthorized flight through the course with even stricter parameters than the original and hitting the target without a wingman, proving that it can be done. Despite the act of insubordination, Cyclone reluctantly appoints Maverick as team leader.

# Maverick flies the lead F/A-18E, accompanied by a buddy-lasing F/A-18F[c] flown by Lieutenant Natasha "Phoenix" Trace and WSO Lieutenant Robert "Bob" Floyd. Rooster leads the second strike pair, which includes Lieutenant Reuben "Payback" Fitch and WSO Lieutenant Mickey "Fanboy" Garcia. The four jets launch from an aircraft carrier, and Tomahawk cruise missiles destroy the nearby air base as they approach. The teams destroy the plant, but the SAMs open fire during their escape. Rooster runs out of countermeasures, and Maverick sacrifices his plane to protect him from an incoming strike. Believing Maverick to be dead, all jets are ordered back to the carrier, but Rooster disobeys and returns to find that Maverick ejected and is being pursued by an Mi-24 attack helicopter. After destroying the gunship, Rooster is shot down by a SAM and ejects. The two rendezvous and steal an F-14 from the damaged air base. Maverick and Rooster destroy two intercepting Su-57s, but a third attacks as they run out of ammunition and countermeasures. Hangman unexpectedly arrives in time to shoot it down, and the planes return safely.

# Later, Rooster helps Maverick work on his P-51 Mustang. Rooster looks at a photo of their mission's success, pinned alongside a photo of his late father and a young Maverick, as Penny and Maverick fly off in the P-51.

# """)