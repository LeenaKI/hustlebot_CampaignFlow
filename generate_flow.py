import json

def build_jubilant_campaign():
    steps = []

    # Helper function to append steps
    def add_step(step):
        steps.append(step)

    # 1. Entry Sequence (Welcome, Name, Phone, City Ask)
    add_step({
        "id": "welcome_message",
        "type": "message",
        "label": "Welcome Msg",
        "config": {
            "messageType": "image",
            "messageConfig": {
                "link": "https://example.com/jubilant_motorworks_welcome.jpg",
                "caption": "Welcome to Jubilant MotorWorks! With over 70+ facilities and 1 million vehicles delivered, we are your trusted automotive partner."
            },
            "onFailureAction": "skip"
        },
        "routing": {"nextStepId": "ask_name"}
    })

    add_step({
        "id": "ask_name",
        "type": "message",
        "label": "Ask Name",
        "config": {
            "messageType": "text",
            "messageConfig": {"content": "To provide you with a personalized experience, could you please share your full name?"},
            "waitForReply": True,
            "replyTimeoutHours": 24,
            "timeoutAction": "exit",
            "saveReplyAs": "customer_name",
            "replyValidation": {
                "matchType": "regex",
                "regexPattern": "^[a-zA-Z\\s]+$",
                "invalidReplyMessage": "Please use letters only."
            }
        },
        "routing": {"nextStepId": "ask_phone"}
    })

    add_step({
        "id": "ask_phone",
        "type": "message",
        "label": "Ask Phone",
        "config": {
            "messageType": "text",
            "messageConfig": {"content": "Thank you! Please share your 10-digit mobile number so our Sales Advisors can reach you."},
            "waitForReply": True,
            "replyTimeoutHours": 24,
            "timeoutAction": "exit",
            "saveReplyAs": "customer_phone",
            "replyValidation": {
                "matchType": "regex",
                "regexPattern": "^\\d{10}$",
                "invalidReplyMessage": "Please enter a valid 10-digit number."
            }
        },
        "routing": {"nextStepId": "ask_city"}
    })

    # 2. City Routing Configuration
    cities = [
        {"id": "city_mumbai", "title": "Mumbai", "prefix": "mum", "intro": "Welcome to our Mumbai division! Our Senior Showroom Coordinators are ready to assist you.", "img_cap": "Experience luxury and performance in Mumbai."},
        {"id": "city_delhi", "title": "Delhi / NCR", "prefix": "del", "intro": "Hello from Delhi NCR! A dedicated Sales Consultant will be assigned to guide your purchase.", "img_cap": "Explore our multi-brand showrooms across Delhi NCR."},
        {"id": "city_bangalore", "title": "Bengaluru", "prefix": "blr", "intro": "Greetings from Bengaluru! Our EV and Luxury Specialists are here to help.", "img_cap": "Leading the EV and premium mobility shift in Bengaluru."},
        {"id": "city_chennai", "title": "Chennai", "prefix": "che", "intro": "Welcome to our Chennai network. A professional Product Advisor will ensure a seamless experience.", "img_cap": "Unmatched after-sales service and delivery in Chennai."},
        {"id": "city_hyderabad", "title": "Hyderabad", "prefix": "hyd", "intro": "Hello Hyderabad! Our certified Dealership Managers are ready to showcase our top-tier vehicles.", "img_cap": "Premium test drive experiences in Hyderabad."},
        {"id": "city_pune", "title": "Pune", "prefix": "pun", "intro": "Welcome to Pune! Let our specialized Client Advisors match you with the perfect vehicle.", "img_cap": "Driving innovation and excellence in Pune."},
        {"id": "city_kolkata", "title": "Kolkata", "prefix": "kol", "intro": "Greetings from Kolkata. Our Regional Sales Consultants will handle your inquiry.", "img_cap": "The largest automotive network in the East."},
        {"id": "city_ahmedabad", "title": "Ahmedabad", "prefix": "ahm", "intro": "Hello Ahmedabad! A dedicated Automotive Specialist will be with you.", "img_cap": "Transparent, high-satisfaction dealerships in Gujarat."}
    ]

    add_step({
        "id": "ask_city",
        "type": "message",
        "label": "Ask City",
        "config": {
            "messageType": "interactive",
            "messageConfig": {
                "body": "Across our 15+ cities of operation, where are you looking to purchase or test drive?",
                "buttonText": "Select City",
                "sections": [{"title": "Dealership Cities", "rows": [{"id": c["id"], "title": c["title"]} for c in cities]}]
            },
            "waitForReply": True,
            "replyTimeoutHours": 24,
            "timeoutAction": "exit",
            "saveReplyAs": "selected_city"
        },
        "routing": {"nextStepId": "city_switch"}
    })

    add_step({
        "id": "city_switch",
        "type": "switch",
        "label": "City Switch",
        "config": {
            "fallbackAction": "continue",
            "switchConfig": {
                "switchOn": "selected_city",
                "cases": {c["id"]: f"{c['prefix']}_intro" for c in cities}
            }
        },
        "routing": {"nextStepId": "ask_brand"}
    })

    # Programmatically generate the branches for all 8 cities
    for c in cities:
        prefix = c["prefix"]
        add_step({
            "id": f"{prefix}_intro",
            "type": "message",
            "label": f"{c['title']} Intro",
            "config": {"messageType": "text", "messageConfig": {"content": c["intro"]}},
            "routing": {"nextStepId": f"{prefix}_img"}
        })
        add_step({
            "id": f"{prefix}_img",
            "type": "message",
            "label": f"{c['title']} Image",
            "config": {
                "messageType": "image",
                "messageConfig": {"link": f"https://example.com/jubilant_{prefix}.jpg", "caption": c["img_cap"]},
                "onFailureAction": "skip"
            },
            "routing": {"nextStepId": f"{prefix}_tag"}
        })
        add_step({
            "id": f"{prefix}_tag",
            "type": "apply_tag",
            "label": f"{c['title']} Tag",
            "config": {"tagConfig": {"tags": [c["id"]]}},
            "routing": {"nextStepId": "ask_brand"}
        })

    # 3. Brand Portfolio Routing
    brands = [
        {"id": "brand_audi", "title": "Audi (Luxury)", "desc": "Premium luxury vehicles", "msg": "Excellent choice. Our authorized Audi dealerships offer an unparalleled luxury purchasing experience.", "tag": "segment_luxury"},
        {"id": "brand_mahindra", "title": "Mahindra SUVs & EV", "desc": "Thar Roxx, XEV 9S", "msg": "Perfect! Whether you want the rugged Thar Roxx or the futuristic XEV 9S, we have the inventory.", "tag": "segment_suv_ev"},
        {"id": "brand_mg", "title": "MG / MG Select", "desc": "Mainstream & Premium", "msg": "Great! Experience connected mobility with MG Motor and premium luxury via MG Select.", "tag": "segment_tech_cars"},
        {"id": "brand_jawa", "title": "Jawa Yezdi", "desc": "Classic Motorcycles", "msg": "Ride into history. As an authorized Jawa Yezdi dealer, we bring classic motorcycles to life.", "tag": "segment_two_wheeler"},
        {"id": "brand_preowned", "title": "Pre-Owned Luxury", "desc": "Certified Used Cars", "msg": "Smart choice. Our Certified Pre-Owned division specializes in rigorously inspected luxury vehicles.", "tag": "segment_used_luxury"}
    ]

    add_step({
        "id": "ask_brand",
        "type": "message",
        "label": "Ask Brand",
        "config": {
            "messageType": "interactive",
            "messageConfig": {
                "body": "Which division of Jubilant MotorWorks are you interested in exploring?",
                "buttonText": "Select Brand",
                "sections": [{"title": "Our Portfolio", "rows": [{"id": b["id"], "title": b["title"], "description": b["desc"]} for b in brands]}]
            },
            "waitForReply": True,
            "replyTimeoutHours": 24,
            "timeoutAction": "exit",
            "saveReplyAs": "selected_brand"
        },
        "routing": {"nextStepId": "brand_switch"}
    })

    add_step({
        "id": "brand_switch",
        "type": "switch",
        "label": "Brand Switch",
        "config": {
            "fallbackAction": "continue",
            "switchConfig": {
                "switchOn": "selected_brand",
                "cases": {b["id"]: f"msg_{b['id'].split('_')[1]}" for b in brands}
            }
        },
        "routing": {"nextStepId": "ask_trade_in"}
    })

    # Programmatically generate brand messaging and tags
    for b in brands:
        b_key = b["id"].split("_")[1]
        add_step({
            "id": f"msg_{b_key}",
            "type": "message",
            "label": f"Msg {b_key.capitalize()}",
            "config": {"messageType": "text", "messageConfig": {"content": b["msg"]}},
            "routing": {"nextStepId": f"tag_{b_key}"}
        })
        add_step({
            "id": f"tag_{b_key}",
            "type": "apply_tag",
            "label": f"Tag {b_key.capitalize()}",
            "config": {"tagConfig": {"tags": [b["id"], b["tag"]]}},
            "routing": {"nextStepId": "ask_trade_in"}
        })

    # 4. Qualification & Post-CTA Sequences (Trade-in, Finance, CTA)
    shared_steps = [
        {
            "id": "ask_trade_in",
            "type": "message",
            "label": "Ask Trade In",
            "config": {
                "messageType": "interactive",
                "messageConfig": {
                    "body": "Do you have an existing vehicle you'd like to trade-in for an upgrade bonus?",
                    "buttons": [{"id": "btn_trade_yes", "title": "Yes, Evaluate It"}, {"id": "btn_trade_no", "title": "No Trade-In"}]
                },
                "waitForReply": True,
                "replyTimeoutHours": 24,
                "timeoutAction": "exit",
                "saveReplyAs": "trade_in_intent"
            },
            "routing": {"nextStepId": "cond_trade_in"}
        },
        {
            "id": "cond_trade_in",
            "type": "condition",
            "label": "Cond Trade In",
            "config": {"conditionConfig": {"type": "button_reply", "buttonId": "btn_trade_yes"}, "fallbackAction": "continue"},
            "routing": {"trueBranchStepId": "trade_yes_msg", "falseBranchStepId": "ask_finance", "nextStepId": ""}
        },
        {
            "id": "trade_yes_msg",
            "type": "message",
            "label": "Trade Yes Msg",
            "config": {"messageType": "text", "messageConfig": {"content": "Perfect. Our certified evaluators will assess your vehicle using advanced diagnostics for the best value."}},
            "routing": {"nextStepId": "ask_finance"}
        },
        {
            "id": "ask_finance",
            "type": "message",
            "label": "Ask Finance",
            "config": {
                "messageType": "interactive",
                "messageConfig": {
                    "body": "We offer quick approval windows for in-house financing. How do you plan to finance your purchase?",
                    "buttons": [{"id": "btn_emi", "title": "Looking for EMI"}, {"id": "btn_cash", "title": "Full Payment"}]
                },
                "waitForReply": True,
                "replyTimeoutHours": 24,
                "timeoutAction": "exit",
                "saveReplyAs": "finance_preference"
            },
            "routing": {"nextStepId": "cond_finance"}
        },
        {
            "id": "cond_finance",
            "type": "condition",
            "label": "Cond Finance",
            "config": {"conditionConfig": {"type": "button_reply", "buttonId": "btn_emi"}, "fallbackAction": "continue"},
            "routing": {"trueBranchStepId": "emi_msg", "falseBranchStepId": "ask_cta", "nextStepId": ""}
        },
        {
            "id": "emi_msg",
            "type": "message",
            "label": "EMI Msg",
            "config": {"messageType": "text", "messageConfig": {"content": "Great! Our advisors will use our EMI Smart Calculator to tailor a payment plan that fits your exact budget."}},
            "routing": {"nextStepId": "ask_cta"}
        },
        {
            "id": "ask_cta",
            "type": "message",
            "label": "Ask CTA",
            "config": {
                "messageType": "interactive",
                "messageConfig": {
                    "body": "What would be the best next step for you?",
                    "buttons": [
                        {"id": "btn_td", "title": "Book Test Drive"},
                        {"id": "btn_advisor", "title": "Talk to Advisor"},
                        {"id": "btn_browse", "title": "Just Browsing"}
                    ]
                },
                "waitForReply": True,
                "replyTimeoutHours": 24,
                "timeoutAction": "exit",
                "saveReplyAs": "primary_cta_intent"
            },
            "routing": {"nextStepId": "cta_switch"}
        },
        {
            "id": "cta_switch",
            "type": "switch",
            "label": "CTA Switch",
            "config": {
                "fallbackAction": "continue",
                "switchConfig": {
                    "switchOn": "primary_cta_intent",
                    "cases": {"btn_td": "td_ask_date", "btn_advisor": "adv_msg", "btn_browse": "browse_msg"}
                }
            },
            "routing": {"nextStepId": "exit_flow"}
        },
        {
            "id": "td_ask_date",
            "type": "message",
            "label": "TD Ask Date",
            "config": {
                "messageType": "interactive",
                "messageConfig": {
                    "body": "Let's get you behind the wheel. When would you like to schedule your test drive?",
                    "buttonText": "Select Date",
                    "sections": [{"title": "Available Dates", "rows": [{"id": "date_today", "title": "Today"}, {"id": "date_tomorrow", "title": "Tomorrow"}, {"id": "date_weekend", "title": "This Weekend"}]}]
                },
                "waitForReply": True,
                "replyTimeoutHours": 24,
                "timeoutAction": "exit",
                "saveReplyAs": "td_date"
            },
            "routing": {"nextStepId": "td_ask_slot"}
        },
        {
            "id": "td_ask_slot",
            "type": "message",
            "label": "TD Ask Slot",
            "config": {
                "messageType": "interactive",
                "messageConfig": {
                    "body": "And what time of day works best for you?",
                    "buttonText": "Select Slot",
                    "sections": [{"title": "Time Slots", "rows": [{"id": "slot_morn", "title": "Morning (10AM-1PM)"}, {"id": "slot_aft", "title": "Afternoon (1PM-4PM)"}, {"id": "slot_eve", "title": "Evening (4PM-7PM)"}]}]
                },
                "waitForReply": True,
                "replyTimeoutHours": 24,
                "timeoutAction": "exit",
                "saveReplyAs": "td_slot"
            },
            "routing": {"nextStepId": "td_confirm"}
        },
        {
            "id": "td_confirm",
            "type": "message",
            "label": "TD Confirm",
            "config": {"messageType": "text", "messageConfig": {"content": "Perfect! Your test drive is confirmed. A Showroom Coordinator will share the exact facility details shortly."}},
            "routing": {"nextStepId": "tag_td"}
        },
        {
            "id": "tag_td",
            "type": "apply_tag",
            "label": "Tag TD",
            "config": {"tagConfig": {"tags": ["test_drive_booked", "high_intent"]}},
            "routing": {"nextStepId": "delay_24h_td"}
        },
        {
            "id": "delay_24h_td",
            "type": "delay",
            "label": "Delay 24h TD",
            "config": {"delayConfig": {"type": "fixed", "delayMs": 86400000}},
            "routing": {"nextStepId": "td_reminder"}
        },
        {
            "id": "td_reminder",
            "type": "message",
            "label": "TD Reminder",
            "config": {"messageType": "text", "messageConfig": {"content": "Hi! Just a friendly reminder about your upcoming test drive. We look forward to hosting you!"}},
            "routing": {"nextStepId": "exit_flow"}
        },
        {
            "id": "adv_msg",
            "type": "message",
            "label": "Advisor Msg",
            "config": {"messageType": "text", "messageConfig": {"content": "Noted! A Senior Consultant will call you shortly to discuss specifications, maintenance packages, and insurance."}},
            "routing": {"nextStepId": "exit_flow"}
        },
        {
            "id": "browse_msg",
            "type": "message",
            "label": "Browse Msg",
            "config": {"messageType": "text", "messageConfig": {"content": "No problem! Take your time. Don't forget to try out the EV savings calculator on our website!"}},
            "routing": {"nextStepId": "exit_flow"}
        },
        {
            "id": "exit_flow",
            "type": "exit",
            "label": "End Flow",
            "config": {},
            "routing": {"nextStepId": ""}
        }
    ]

    for step in shared_steps:
        add_step(step)

    # Wrap in final payload
    return {"steps": steps}

# ---------------------------------------------------------
# EXECUTION & EXPORT
# ---------------------------------------------------------
if __name__ == "__main__":
    campaign_json = build_jubilant_campaign()
    
    # 1. Print the JSON to the console
    json_string = json.dumps(campaign_json, indent=2)
    print("Campaign JSON successfully generated!")
    
    # 2. Save it directly to a file
    file_name = "jubilant_whatsapp_campaign.json"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(json_string)
        
    print(f"File saved locally as: {file_name}")
    print(f"Total steps generated: {len(campaign_json['steps'])}")