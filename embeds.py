import discord


# Update this
def vision():
    embed = discord.Embed(title="Company Goals (Vision 2020)",
                      description="Goals are used to help a business grow and achieve its objectives. They can be used "
                                  "to foster teamwork and help the business describe what it wants to accomplish in a "
                                  "specific time period. Setting up goals is an important part of business plan.")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/709710821382553640"
                            "/K_with_bg_1.png")  # Koders Logo
    embed.add_field(name="Hire people to move forward effectively",
                    value="Grow your team from 9 to 20 internal members to reduce burden and achieve goals",
                    inline=False)
    embed.add_field(name="Customer Support & Feedback",
                    value="Focus on making your customer service process exceptional, handling customer complaints "
                          "more effectively, or incorporating customer service into your social media practices. And "
                          "don't forget about the power of asking your customers for feedback in order to identify "
                          "what your business can be doing better.",
                    inline=False)
    embed.add_field(name="Increase traffic on Website & Blogs",
                    value="More website traffic often translates into customer loyalty. Once you have relevant and "
                          "engaging content ready to share on your website or blog. Try to post at least 2-3 blogs "
                          "per week to keep the audience engaged.",
                    inline=False)
    embed.add_field(name="Social Media Marketing",
                    value="Effective use of Social Media Marketing once the landing page of website is ready.",
                    inline=False)
    embed.add_field(name="Projects",
                    value="Minimum of 40-50 Completed Projects should be added in the database from freelancer "
                          "itself.  Look forward to more offline long term clients.  Small scale free Projects should "
                          "be delivered every month in the form of CSR Activity.  At least 7 big projects should be "
                          "completed.",
                    inline=False)
    embed.add_field(name="Portfolio",
                    value="Interns should create some boilerplate projects that are eye candy and can be added in the "
                          "portfolio.",
                    inline=False)
    embed.add_field(name="Risk Management", value="Mechanism required to mitigate downfalls of workflow.", inline=False)
    embed.add_field(name="Media Connection",
                    value="More than 100 Colleges should be added in the 3rd Party for Promotion and Projects  CSR "
                          "Activities should be performed once in a while  Government Projects are welcome to "
                          "increase the reach",
                    inline=False)
    embed.add_field(name="Finances", value="Have a Capital of around Ten Lakhs at the end of Year 2020.", inline=False)
    embed.add_field(name="Thorough SWOT Analysis", value="Yet to research", inline=False)
    embed.add_field(name="Market Research", value="Yet to research", inline=False)
    embed.add_field(name="Employee Incentive Program",
                    value="Keeping up the morale and motivating your employees to work hard in your business can be a "
                          "challenge. Don't have to be more finance driven but small perks can be a big game changer.",
                    inline=False)
    embed.set_footer(text="Last refreshed by Xhunter at 12:39 am Wednesday, 17 June 2020 (IST)")
    return embed


def attendance(opening_time, closing_time):
    embed = discord.Embed(title="Attendance System",
                          description="Please react before closing time else the message will disappear ",
                          color=0x1f65a3)
    embed.set_author(name="Mark you attendance by reacting ⬆️ emoji")
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455"
            "&height=447")
    embed.add_field(name="Opening Time", value=opening_time, inline=False)
    embed.add_field(name="Closing Time", value=closing_time, inline=False)
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed


def attendance_dm(date, time, day):
    embed = discord.Embed(title="Thank you for marking you attendance!", color=0x40e791)
    embed.set_author(name="Attendance")
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455"
            "&height=447")
    embed.add_field(name="Date", value=date, inline=True)
    embed.add_field(name="Time", value=time,  inline=True)
    embed.add_field(name="Day", value=day, inline=True)
    return embed

def attendance_missed_dm(date, time, day):
    embed = discord.Embed(title="Yo have not marked your attendance yet. Only 5 minutes remaining", color=0x40e791)
    embed.set_author(name="Attendance")
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455"
            "&height=447")
    embed.add_field(name="Date", value=date, inline=True)
    embed.add_field(name="Time", value=time,  inline=True)
    embed.add_field(name="Day", value=day, inline=True)
    return embed