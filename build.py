#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for the Dr. Dharmalingam Muthiah (dharmaortho.my) rebuild.
Produces: index.html, about.html, services.html, gallery.html, contact.html,
and services/<slug>.html for each of the 13 services.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Content data
# ---------------------------------------------------------------------------

SERVICES = [
    dict(
        slug="orthopedic-and-trauma-surgery",
        icon="🩺",
        title="Orthopaedic Trauma Surgery",
        short="Expert surgical management of fractures and traumatic musculoskeletal injuries.",
        intro=[
            "Traumatic injuries require prompt assessment and expert orthopaedic care to minimise complications and restore function. We specialise in the management of fractures and complex musculoskeletal injuries resulting from road traffic accidents, falls, sports injuries and workplace trauma.",
            "Every injury is unique. Our treatment approach focuses on accurate diagnosis, timely intervention and personalised rehabilitation plans to help patients recover safely, regain mobility and return to their normal daily activities as quickly as possible.",
        ],
        includes_title="Our Orthopaedic Trauma Services Include",
        includes=[
            ("Simple & Complex Fracture Fixation", "Surgical and non-surgical management of simple, displaced and complex fractures using modern fixation techniques to promote optimal bone healing and restore stability."),
            ("Bone Reconstruction", "Comprehensive treatment for complex bone injuries requiring reconstruction to restore alignment, strength and function following severe trauma."),
            ("Trauma-Related Soft Tissue Injuries", "Assessment and treatment of ligament, tendon, muscle and soft tissue injuries associated with fractures and traumatic accidents to support complete recovery."),
            ("Post-Traumatic Rehabilitation Planning", "Individualised rehabilitation programmes designed to improve strength, mobility and function while reducing recovery time and supporting a safe return to everyday activities."),
        ],
        closing_title="Restoring Function. Rebuilding Lives.",
        closing_text="Our goal is to restore movement, reduce pain and help patients recover confidently following traumatic injuries. By combining advanced orthopaedic techniques with comprehensive rehabilitation planning, we strive to achieve faster healing, safer recovery and the best possible long-term outcomes for every patient.",
    ),
    dict(
        slug="joint-replacement-services",
        icon="🦿",
        title="Joint Replacement Surgery",
        short="Advanced joint replacement procedures to restore function and mobility.",
        intro=[
            "Joint replacement surgery is an effective solution for patients experiencing persistent joint pain, stiffness and reduced mobility caused by advanced arthritis, injury or degenerative joint conditions. When conservative treatments are no longer effective, joint replacement can help restore movement, relieve pain and significantly improve quality of life.",
            "We provide comprehensive assessment and personalised treatment plans using modern surgical techniques and evidence-based care. Every patient receives an individualised approach aimed at achieving the best possible functional outcome and a faster return to daily activities.",
        ],
        includes_title="Our Joint Replacement Services Include",
        includes=[
            ("Hip Replacement Surgery", "Advanced surgical treatment for damaged hip joints to relieve chronic pain, improve mobility and restore normal function."),
            ("Knee Replacement Surgery", "Partial and total knee replacement procedures designed to reduce pain, improve joint stability and help patients regain an active lifestyle."),
            ("Revision Joint Replacement", "Assessment and management of previously replaced joints requiring further surgery due to wear, loosening, infection or implant-related complications."),
            ("Preoperative Assessment & Planning", "Thorough evaluation, diagnostic imaging and personalised surgical planning to ensure the most appropriate treatment for each patient's condition and lifestyle."),
            ("Postoperative Rehabilitation", "Comprehensive rehabilitation programmes focused on restoring strength, flexibility, balance and confidence following joint replacement surgery."),
        ],
        closing_title="Helping You Move Comfortably Again",
        closing_text="Our goal is to relieve pain, restore joint function and improve your quality of life through advanced joint replacement surgery and personalised rehabilitation. From your initial consultation through recovery, we are committed to providing compassionate care and supporting you every step of your journey towards renewed mobility and independence.",
    ),
    dict(
        slug="general-orthopaedic-services",
        icon="🦴",
        title="General Orthopaedic Services",
        short="Comprehensive diagnosis and treatment for bone, joint, muscle, tendon and ligament conditions.",
        intro=[
            "From common bone and joint conditions to complex musculoskeletal disorders, our practice provides comprehensive orthopaedic assessment, accurate diagnosis and personalised treatment plans tailored to each patient's individual needs and lifestyle.",
            "We focus on relieving pain, restoring mobility, improving function and helping patients return to their daily activities safely and confidently through evidence-based orthopaedic care.",
        ],
        includes_title="Our General Orthopaedic Services Include",
        includes=[
            ("Joint Pain & Arthritis", "Assessment and treatment for osteoarthritis, inflammatory arthritis and chronic joint pain affecting the shoulder, hip, knee, elbow, wrist and ankle."),
            ("Bone & Muscle Disorders", "Diagnosis and management of musculoskeletal conditions involving bones, muscles and connective tissues."),
            ("Ligament & Tendon Injuries", "Comprehensive care for sprains, strains, tendon tears and ligament injuries using both non-surgical and surgical treatment options."),
            ("Sports-Related Injuries", "Expert management of acute and overuse injuries to help athletes and active individuals recover and return to peak performance."),
            ("Fractures & Trauma", "Assessment, fracture management and follow-up care for simple and complex bone injuries resulting from accidents or falls."),
            ("Degenerative Musculoskeletal Conditions", "Long-term treatment strategies for age-related joint degeneration, chronic pain and reduced mobility."),
        ],
        closing_title="Personalised Orthopaedic Care",
        closing_text="Every patient receives an individualised treatment plan that may include lifestyle modification, medication, physiotherapy, rehabilitation, minimally invasive procedures or surgery when required. Our goal is to deliver compassionate, evidence-based orthopaedic care that supports long-term joint health, restores mobility and improves overall quality of life.",
    ),
    dict(
        slug="hip-replacement",
        icon="🦵",
        title="Hip Replacement",
        short="Modern hip replacement solutions tailored to each patient's needs.",
        intro=[
            "Hip replacement is a highly successful procedure designed to relieve chronic hip pain, restore movement and improve quality of life for patients with severe arthritis, fractures and degenerative hip conditions.",
            "Using contemporary surgical techniques, comprehensive preoperative planning and structured rehabilitation support, we provide a personalised treatment journey designed around each patient's condition and goals throughout recovery.",
        ],
        includes_title="Benefits of Hip Replacement",
        includes=[
            ("Pain Relief", "Significant relief from chronic pain caused by arthritis and other degenerative hip diseases."),
            ("Enhanced Mobility", "Improved mobility and flexibility, making daily tasks easier and more comfortable."),
            ("Improved Quality of Life", "A renewed sense of independence and the ability to enjoy everyday activities again."),
            ("Long-Lasting Results", "Durable outcomes with modern implants designed for long-term performance."),
        ],
        closing_title="A Personalised Path to Recovery",
        closing_text="Every hip replacement journey is tailored to the individual — from detailed preoperative planning through to structured postoperative rehabilitation — helping patients return to a comfortable, active and independent lifestyle with confidence.",
    ),
    dict(
        slug="velys-tm-robotic-assisted-robotic-assisted",
        icon="🤖",
        title="VELYS™ Robotic-Assisted Knee Replacement",
        short="VELYS™ robotic-assisted technology for enhanced surgical precision.",
        intro=[
            "Experience the next generation of knee replacement surgery with the VELYS™ Robotic-Assisted Solution. Combining advanced robotic technology with surgical expertise, Dr. Dharmalingam Muthiah provides a personalised approach to total knee replacement, helping patients achieve improved implant positioning, enhanced joint function and greater confidence in their recovery.",
            "Every knee is unique. The VELYS™ system allows precise planning and real-time surgical guidance tailored to your individual anatomy — supporting accurate implant placement, reduced discomfort, optimised movement and improved long-term outcomes while enabling a faster return to everyday activities.",
        ],
        includes_title="Benefits of VELYS™ Robotic-Assisted Knee Replacement",
        includes=[
            ("Greater Precision", "Advanced robotic guidance assists with highly accurate implant positioning and alignment, helping to optimise joint balance, improve movement and support long-term implant performance."),
            ("Less Pain", "Minimally invasive surgical techniques help preserve healthy bone and surrounding soft tissues, reducing postoperative discomfort and promoting a smoother healing process."),
            ("Faster Recovery", "Many patients are able to regain mobility sooner, return to their daily activities with greater confidence and experience an improved quality of life following surgery."),
        ],
        closing_title="Regain Your Active Lifestyle",
        closing_text="If knee arthritis is affecting your mobility, comfort and independence, VELYS™ Robotic-Assisted Knee Replacement offers an advanced treatment option focused on precision, comfort and long-term function — helping you move more naturally and return to the activities you enjoy with renewed confidence.",
    ),
    dict(
        slug="arthroscopic-sports-surgery",
        icon="🏃",
        title="Arthroscopic (Keyhole) Sports Surgery",
        short="Minimally invasive treatment for sports injuries and ligament reconstruction.",
        intro=[
            "Arthroscopy, commonly known as keyhole surgery, is a minimally invasive surgical technique used to diagnose and treat a wide range of joint conditions through small incisions. Using a tiny camera and specialised instruments, arthroscopic surgery allows precise treatment while minimising damage to surrounding tissues.",
            "Compared to conventional open surgery, arthroscopy generally offers less postoperative pain, smaller scars, reduced risk of complications and a faster recovery — particularly beneficial for active individuals and athletes who wish to return safely to work, sports and their everyday activities.",
        ],
        includes_title="Arthroscopic Procedures We Perform",
        includes=[
            ("Shoulder Arthroscopy", "Minimally invasive treatment for rotator cuff tears, shoulder instability, frozen shoulder and labral injuries, helping restore strength, stability and range of motion."),
            ("Elbow Arthroscopy", "Management of tennis elbow, ligament injuries, loose bodies and elbow stiffness, with the aim of relieving pain and improving joint function."),
            ("Wrist Arthroscopy", "Treatment for ligament injuries, cartilage damage, chronic wrist pain and sports-related wrist injuries, allowing accurate diagnosis and targeted treatment."),
            ("Hip Arthroscopy", "Surgical management of hip impingement, labral tears and hip instability, helping preserve the natural hip joint while improving movement and reducing discomfort."),
            ("Knee Arthroscopy", "Treatment of meniscus tears, ACL and ligament injuries, cartilage damage, sports injuries and loose bodies, supporting faster recovery and a safe return to physical activity."),
        ],
        closing_title="Minimally Invasive. Faster Recovery.",
        closing_text="Our goal is to restore joint function while minimising pain and recovery time through advanced arthroscopic techniques. Every patient receives a personalised treatment and rehabilitation plan tailored to their condition, activity level and recovery goals.",
    ),
    dict(
        slug="hand-ankle-surgery",
        icon="✋",
        title="Hand & Ankle Surgery",
        short="Specialist care for hand, wrist, foot and ankle conditions.",
        intro=[
            "Conditions affecting the hand and ankle can significantly impact mobility, strength and everyday activities. Whether caused by injury, repetitive strain, sports participation or age-related degeneration, these conditions require specialised assessment and treatment to restore normal function and reduce pain.",
            "We provide comprehensive surgical and non-surgical management for a wide range of hand and ankle conditions, using modern orthopaedic techniques and personalised rehabilitation programmes to help patients regain movement and return confidently to work, sports and daily life.",
        ],
        includes_title="Conditions We Treat",
        includes=[
            ("Tendon Injuries", "Expert management of tendon tears, ruptures and overuse injuries affecting the hand, wrist, ankle and foot to restore strength, flexibility and normal movement."),
            ("Ligament Injuries", "Treatment for ligament sprains, instability and complete ligament tears using both conservative care and advanced surgical reconstruction when required."),
            ("Fractures", "Comprehensive assessment and treatment of simple and complex fractures involving the hand, fingers, wrist, ankle and foot to promote proper healing and restore function."),
            ("Nerve Compression Syndromes", "Diagnosis and treatment of nerve compression conditions, including carpal tunnel syndrome and other peripheral nerve disorders that cause pain, numbness and weakness."),
            ("Degenerative Conditions", "Management of arthritis and other degenerative disorders affecting the hand and ankle to relieve pain, improve joint mobility and maintain function."),
            ("Sports Injuries", "Treatment of acute and chronic sports-related injuries involving the hand, wrist, ankle and foot, with a focus on safe recovery and return to sporting activities."),
        ],
        closing_title="Restoring Movement. Strengthening Recovery.",
        closing_text="Our approach combines accurate diagnosis, advanced surgical expertise and personalised rehabilitation to achieve the best possible outcomes — helping every patient regain strength, restore function and return to an active, independent lifestyle.",
    ),
    dict(
        slug="soft-tissue-tumours",
        icon="🔬",
        title="Soft Tissue Tumours",
        short="Diagnosis and management of benign and malignant soft tissue tumours.",
        intro=[
            "Soft tissue lumps and tumours can develop in muscles, fat, tendons, ligaments and other connective tissues throughout the body. While many soft tissue lumps are benign, some require further investigation to determine their nature and ensure appropriate treatment.",
            "We provide comprehensive assessment and management of soft tissue tumours using a systematic approach that includes clinical evaluation, appropriate investigations and personalised treatment planning, with a priority on accurate diagnosis and safe, effective care.",
        ],
        includes_title="Our Soft Tissue Tumour Services Include",
        includes=[
            ("Clinical Evaluation", "A thorough consultation and physical examination to assess the size, location, characteristics and symptoms of soft tissue lumps, helping determine the most appropriate next steps."),
            ("Diagnostic Assessment", "Appropriate diagnostic investigations, including imaging studies and other necessary assessments, to accurately identify the nature of the soft tissue tumour and guide treatment planning."),
            ("Surgical Removal of Suitable Soft Tissue Tumours", "Careful surgical excision of suitable benign and selected soft tissue tumours using techniques that prioritise complete removal, functional preservation and optimal healing."),
            ("Ongoing Follow-Up Care", "Regular postoperative reviews and long-term monitoring to assess healing, recovery and detect any recurrence or concerns, ensuring continued patient wellbeing."),
        ],
        closing_title="Early Assessment Leads to Better Outcomes",
        closing_text="Early evaluation of soft tissue lumps is important to determine whether they require observation, further investigation or surgical treatment. We are committed to providing timely diagnosis, personalised treatment and comprehensive follow-up care.",
    ),
    dict(
        slug="musculoskeletal-infections",
        icon="🦠",
        title="Musculoskeletal Infections",
        short="Comprehensive treatment for bone, joint and soft tissue infections.",
        intro=[
            "Musculoskeletal infections involving the bones, joints and surrounding soft tissues require early diagnosis and prompt treatment to prevent long-term complications. If left untreated, these infections may lead to chronic pain, joint damage, reduced mobility and permanent loss of function.",
            "We provide comprehensive assessment and management for a wide range of musculoskeletal infections, combining accurate diagnosis, evidence-based treatment and personalised rehabilitation to help patients recover safely.",
        ],
        includes_title="Our Musculoskeletal Infection Services Include",
        includes=[
            ("Clinical Assessment", "Comprehensive evaluation of symptoms, medical history and physical examination to identify signs of bone, joint or soft tissue infection and determine the severity of the condition."),
            ("Diagnostic Investigations", "Appropriate laboratory tests, imaging studies and other diagnostic investigations are performed to accurately identify the source of infection and guide the most effective treatment plan."),
            ("Medical & Surgical Management", "Treatment may include antibiotic therapy, surgical drainage, removal of infected tissue or other orthopaedic procedures where necessary to eliminate infection and preserve joint and bone function."),
            ("Infection Control & Rehabilitation", "Ongoing monitoring, infection control measures and structured rehabilitation programmes are provided to support recovery, restore mobility and reduce the risk of recurrence."),
        ],
        closing_title="Prompt Diagnosis. Effective Treatment. Lasting Recovery.",
        closing_text="Early diagnosis and appropriate treatment are essential for achieving the best possible outcomes in musculoskeletal infections. Our approach focuses on controlling infection, preserving healthy bone and joint function, and helping patients return to their normal daily activities with confidence.",
    ),
    dict(
        slug="specialist-assessment-management",
        icon="📋",
        title="Specialist Assessment & Management",
        short="Personalised consultations, diagnosis and long-term orthopaedic management.",
        intro=[
            "Not every orthopaedic condition requires surgery. We provide comprehensive specialist assessment and personalised non-operative management for a wide range of musculoskeletal disorders, helping patients achieve pain relief, improved mobility and a better quality of life through evidence-based treatment.",
            "Every patient receives a thorough clinical evaluation, supported by appropriate investigations where necessary, to identify the underlying cause of their symptoms and develop an individualised treatment plan that avoids unnecessary surgery whenever possible.",
        ],
        includes_title="Comprehensive Orthopaedic Assessment",
        includes=[
            ("Clinical Evaluation", "Detailed assessment of your symptoms, medical history and physical examination to accurately diagnose orthopaedic conditions and recommend the most appropriate treatment options."),
            ("Non-Operative Management", "Personalised treatment plans may include medication, physiotherapy, lifestyle modification, rehabilitation and other conservative treatment approaches aimed at relieving pain and restoring function."),
            ("Neck & Back Pain (Spinal Disorders)", "Assessment and management of acute and chronic neck and back pain, sciatica and degenerative spinal conditions affecting the cervical, thoracic and lumbar spine."),
            ("Referral for Complex Spinal Surgery", "Patients requiring specialised spinal procedures or complex spinal surgery will be referred to experienced spine specialists to ensure they receive the most appropriate expert care."),
        ],
        closing_title="Expert Care. Personalised Treatment.",
        closing_text="Our goal is to provide accurate diagnosis, effective non-operative treatment and clear guidance to help patients manage orthopaedic conditions with confidence — focusing on conservative care whenever surgery is not required.",
    ),
    dict(
        slug="paediatric-orthopaedic-disorders",
        icon="👶",
        title="Paediatric Orthopaedic Disorders",
        short="Assessment and management of orthopaedic conditions in growing children.",
        intro=[
            "Children's bones, joints and muscles are continually growing and developing, making paediatric orthopaedic conditions different from those seen in adults. Early assessment is essential to identify developmental problems, guide appropriate treatment and support healthy growth while preventing long-term complications.",
            "We provide comprehensive evaluation and management of a wide range of paediatric orthopaedic conditions, with every child receiving an individualised assessment tailored to their age, stage of development and specific condition.",
        ],
        includes_title="Our Paediatric Orthopaedic Services Include",
        includes=[
            ("Limb Deformities", "Assessment and management of congenital and developmental limb deformities affecting the arms or legs, with treatment plans designed to support healthy growth and function."),
            ("Walking Abnormalities", "Evaluation of gait abnormalities, limping, in-toeing, out-toeing and other walking concerns to determine the underlying cause and recommend appropriate management."),
            ("Developmental Bone Conditions", "Diagnosis and treatment of developmental bone and joint disorders, ensuring early intervention where necessary to promote normal growth and mobility."),
            ("Paediatric Fractures", "Comprehensive care for fractures in children, with treatment focused on proper bone healing while protecting future growth and development."),
        ],
        closing_title="Supporting Healthy Growth & Development",
        closing_text="Our goal is to provide timely diagnosis, compassionate care and personalised treatment that supports every child's healthy musculoskeletal development, working closely with parents and caregivers throughout.",
    ),
    dict(
        slug="bone-tumours",
        icon="🩻",
        title="Bone Tumours",
        short="Careful evaluation and coordinated care for suspected bone tumours.",
        intro=[
            "Bone tumours and bone lesions require careful evaluation to determine their nature and the most appropriate course of treatment. While many bone lesions are benign, some require further investigation to establish an accurate diagnosis and ensure timely management.",
            "We provide comprehensive assessment for patients with suspected bone tumours, using a structured approach that combines clinical evaluation, imaging review and coordinated investigations, with treatment recommendations based on each patient's individual condition.",
        ],
        includes_title="Our Bone Tumour Services Include",
        includes=[
            ("Clinical Evaluation", "A thorough medical history and physical examination are performed to assess symptoms, identify potential risk factors and determine the most appropriate diagnostic pathway."),
            ("Imaging Review", "Detailed review of X-rays, CT scans, MRI scans and other relevant imaging studies to evaluate bone abnormalities and guide further assessment."),
            ("Initial Management", "Individualised treatment planning and early management to address symptoms, protect bone integrity and determine whether additional investigations or intervention are required."),
            ("Coordination of Further Investigations", "Arrangement and coordination of additional diagnostic tests, including advanced imaging and biopsy where appropriate, to establish a definitive diagnosis and guide ongoing care."),
        ],
        closing_title="Early Diagnosis. Expert Guidance. Personalised Care.",
        closing_text="Patients requiring specialised bone tumour surgery or advanced orthopaedic oncology care will be referred to recognised orthopaedic oncology specialists, ensuring comprehensive treatment and reassurance throughout every stage of the journey.",
    ),
    dict(
        slug="collaborative-specialist-care",
        icon="🤝",
        title="Collaborative Specialist Care",
        short="Coordinated referral to trusted subspecialists for complex conditions.",
        intro=[
            "Some orthopaedic conditions require highly specialised expertise and multidisciplinary management to achieve the best possible outcomes. We believe every patient deserves access to the most appropriate level of care, particularly when advanced surgical intervention is required.",
            "When complex conditions extend beyond the scope of general orthopaedic practice, we work closely with experienced, peer-recognised orthopaedic subspecialists to ensure patients receive seamless care and ongoing support throughout every stage of their recovery.",
        ],
        includes_title="Our Collaborative Care Approach",
        includes=[
            ("Advanced Spinal Disorders", "Patients with complex spinal conditions requiring specialised spinal surgery will be referred to experienced spine surgeons with advanced expertise in cervical, thoracic and lumbar spinal disorders."),
            ("Paediatric Orthopaedic Conditions", "Children with complex congenital, developmental or surgical orthopaedic conditions are referred to dedicated paediatric orthopaedic specialists for age-appropriate treatment."),
            ("Bone Tumours & Orthopaedic Oncology", "Patients requiring specialised bone tumour surgery or advanced orthopaedic oncology management will be referred to recognised orthopaedic oncology specialists."),
            ("Coordinated Patient Care", "We work closely with trusted specialists and healthcare professionals to coordinate investigations, referrals, treatment planning and postoperative follow-up."),
        ],
        closing_title="Working Together for the Best Possible Outcomes",
        closing_text="By working in partnership with experienced subspecialty orthopaedic surgeons and multidisciplinary healthcare teams, we ensure every patient receives personalised, coordinated and evidence-based care that supports the best possible recovery.",
    ),
]

SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}

# Order shown on the homepage preview grid (9 of the 13, matches most-requested procedures)
HOME_PREVIEW_SLUGS = [
    "general-orthopaedic-services",
    "orthopedic-and-trauma-surgery",
    "joint-replacement-services",
    "hip-replacement",
    "velys-tm-robotic-assisted-robotic-assisted",
    "arthroscopic-sports-surgery",
    "hand-ankle-surgery",
    "musculoskeletal-infections",
    "specialist-assessment-management",
]

NAV_ITEMS = [
    ("Home", "/index.html"),
    ("About Dr", "/about.html"),
]

CONTACT = dict(
    address_lines=["Suite 02-06, Level 6", "Riverson@Sembulan, Block A-1", "Lorong Riverson@Sembulan, Off Coastal Highway", "88100 Kota Kinabalu, Sabah"],
    whatsapp="+60 11-3666 1140",
    whatsapp_href="https://wa.me/601136661140",
    phone="+60 88-518 879",
    phone_href="tel:+6088518879",
    email="enquiry@dharmaortho.my",
    hours=[("Monday – Friday", "9:00 AM – 5:00 PM"), ("Saturday", "9:00 AM – 1:00 PM")],
    facebook="https://facebook.com/dharmaortho",
    instagram="https://instagram.com/orthodm",
)

# Consultation booking: clinic is open Monday-Saturday, closed Sunday.
# Slot lists below are rendered client-side in js/main.js depending on the
# weekday of the date the patient picks; keep in sync if hours ever change.
BOOKING_SLOTS = {
    "weekday": ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
                "12:00 PM", "12:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM"],
    "saturday": ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
                 "12:00 PM", "12:30 PM"],
}
BOOKING_EMAIL = "appointment@dharmaortho.my"

# Real clinical case photos pulled from the live site's picture gallery,
# grouped by case. Each case renders as a card in the Image Gallery; clicking
# it opens a lightbox to browse every photo in that case.
GALLERY_CASES = [
    {
        "slug": "knee-replacement",
        "title": "Total Knee Replacement",
        "desc": "Pre- and post-operative imaging showing implant positioning and alignment.",
        "count": 4,
        "cover": 1,
    },
    {
        "slug": "hip-replacement",
        "title": "Total Hip Replacement",
        "desc": "Case series showing restored hip joint anatomy after total replacement.",
        "count": 4,
    },
    {
        "slug": "medial-osteoarthritis",
        "title": "Severe Medial Compartment Osteoarthritis",
        "desc": "Progressive joint space narrowing and degenerative change in the medial knee compartment.",
        "count": 5,
    },
    {
        "slug": "quadriceps-rupture",
        "title": "Neglected Quadriceps Tendon Rupture",
        "desc": "Surgical repair of a delayed-presentation quadriceps tendon injury.",
        "count": 6,
    },
    {
        "slug": "erl-rupture",
        "title": "Spontaneous ERL Rupture in a 24-Year-Old",
        "desc": "Tendon rupture repair in a young patient, from diagnosis through surgical correction.",
        "count": 6,
        "cover": 4,
    },
    {
        "slug": "tibia-stress-fracture",
        "title": "Stress Fracture of the Tibia",
        "desc": "Imaging and management of an overuse stress fracture of the tibia.",
        "count": 3,
    },
    {
        "slug": "mcl-tear",
        "title": "MCL Substance Tear",
        "desc": "Medial collateral ligament injury assessment.",
        "count": 1,
    },
    {
        "slug": "ulnar-nerve-decompression",
        "title": "Ulnar Nerve Decompression",
        "desc": "Surgical decompression of the ulnar nerve at Guyon's tunnel.",
        "count": 2,
    },
    {
        "slug": "giant-cell-tumour",
        "title": "Giant Cell Tumour of Tendon Sheath",
        "desc": "Excision of a benign soft-tissue tumour of the tendon sheath.",
        "count": 1,
    },
]
for _c in GALLERY_CASES:
    _c["images"] = [f"{_c['slug']}-{i}.jpg" for i in range(1, _c["count"] + 1)]

# Video Gallery — real case-highlight videos from Dr. Dharmalingam's own
# YouTube channel (@DHARMA240), embedded via YouTube's privacy-enhanced player.
YOUTUBE_CHANNEL = "https://www.youtube.com/@DHARMA240"
VIDEOS = [
    {"id": "qVd4bJbRnPA", "title": "A 20-year-old woman presented with a knee injury sustained during netball"},
    {"id": "_MCxCibJGco", "title": "A 13-year-old with severe low back pain — what's the cause?"},
    {"id": "xMft-TFGWTk", "title": "A 45-year-old gentleman presented with right groin-to-thigh pain of insidious onset"},
    {"id": "OHd_6hhK3L8", "title": "Severe knee recurvatum — regaining stability through knee replacement"},
    {"id": "qZXjEkS6i10", "title": "A 7-year-old boy with a traumatic amputation of the fingertip"},
    {"id": "IRyvRaUsIig", "title": "A 29-year-old gentleman with persistent pain over the outer side of his right knee"},
    {"id": "752VoYSd44o", "title": "Avascular necrosis (AVN) of the hip"},
    {"id": "31p4F72HhuA", "title": "A meniscus tear in a 35-year-old patient"},
    {"id": "aT3eIgIWa94", "title": "What is Ledderhose disease?"},
    {"id": "9qveREndO90", "title": "A young patient with osteochondrosis dissecans of the talus"},
    {"id": "b9C204Gb4Us", "title": "A 21-year-old with an acute knee injury from playing basketball"},
    {"id": "hwsT-BbfYes", "title": "Charcot neuro-osteoarthropathy (Charcot joint)"},
]

# ---------------------------------------------------------------------------
# Shared markup helpers
# ---------------------------------------------------------------------------

def icon_svg(name):
    icons = {
        "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
        "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>',
        "whatsapp": '<svg viewBox="0 0 32 32" fill="currentColor"><path d="M16.001 3C9.373 3 4 8.373 4 15c0 2.317.646 4.482 1.77 6.33L4 29l7.86-1.73A11.94 11.94 0 0 0 16 27c6.627 0 12-5.373 12-12S22.628 3 16.001 3Zm0 21.818A9.78 9.78 0 0 1 10.9 23.4l-.365-.217-4.664 1.028 1.05-4.548-.238-.373A9.78 9.78 0 0 1 6.18 15c0-5.415 4.406-9.818 9.82-9.818 5.415 0 9.818 4.403 9.818 9.818 0 5.415-4.403 9.818-9.818 9.818Zm5.4-7.352c-.296-.148-1.75-.864-2.022-.963-.271-.099-.469-.148-.667.148-.198.296-.766.963-.94 1.161-.173.198-.346.223-.642.075-.296-.148-1.25-.46-2.38-1.467-.88-.785-1.474-1.754-1.647-2.05-.173-.297-.019-.457.13-.604.133-.133.297-.346.445-.52.148-.173.198-.296.297-.494.099-.198.05-.371-.025-.52-.074-.148-.667-1.608-.914-2.202-.24-.578-.485-.5-.667-.51l-.568-.01a1.09 1.09 0 0 0-.79.37c-.272.297-1.04 1.016-1.04 2.478s1.065 2.874 1.213 3.072c.148.198 2.096 3.2 5.08 4.488.71.306 1.263.489 1.694.626.712.227 1.36.195 1.872.118.571-.085 1.75-.715 1.997-1.406.247-.692.247-1.285.173-1.407-.074-.123-.272-.198-.568-.346Z"/></svg>',
        "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s7-6.06 7-12A7 7 0 0 0 5 10c0 5.94 7 12 7 12Z"/><circle cx="12" cy="10" r="2.4"/></svg>',
        "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a2 2 0 0 1-2 2C9.5 21 3 14.5 3 6a2 2 0 0 1 1-2Z"/></svg>',
        "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
        "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
        "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6l7-3Z"/></svg>',
        "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7.5-4.9-10-9.3C.6 8.2 2 4.8 5.4 4.1 7.7 3.6 10 4.7 12 7c2-2.3 4.3-3.4 6.6-2.9 3.4.7 4.8 4.1 3.4 7.6C19.5 16.1 12 21 12 21Z"/></svg>',
        "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2v4M12 18v4M4 12H2M22 12h-2M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/><circle cx="12" cy="12" r="4"/></svg>',
        "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 22v-8.5H16l.5-3.5h-3V7.7c0-1 .3-1.7 1.7-1.7H16.6V2.8C16.3 2.7 15.3 2.6 14.1 2.6c-2.5 0-4.2 1.5-4.2 4.3V10H7.4v3.5H10V22h3.5Z"/></svg>',
        "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>',
        "chevron": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
        "image": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="1.8"/><path d="m21 15-5-5L5 21"/></svg>',
        "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.14v13.72a1 1 0 0 0 1.52.85l11-6.86a1 1 0 0 0 0-1.7l-11-6.86A1 1 0 0 0 8 5.14Z"/></svg>',
        "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    }
    return icons.get(name, "")


def services_dropdown_html(current_slug=None, prefix="/"):
    items = []
    for s in SERVICES:
        href = f"{prefix}services/{s['slug']}.html"
        cls = ' class="active"' if s["slug"] == current_slug else ""
        items.append(f'<a href="{href}"{cls}>{s["icon"]} {s["title"]}</a>')
    return "\n".join(items)


def header_html(active="", prefix="", current_slug=None):
    def cls(name):
        return ' class="active"' if active == name else ""

    nav_services_active = ' class="active"' if active == "services" else ""
    return f"""
<header class="site-header">
  <div class="topbar">
    <div class="container">
      <div class="topbar-links">
        <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener">WhatsApp <span data-cms="contact.whatsapp_display">{CONTACT['whatsapp']}</span></a>
        <a href="{CONTACT['phone_href']}" data-cms-href="contact.phone_href">Clinic: <span data-cms="contact.phone_display">{CONTACT['phone']}</span></a>
        <a href="mailto:{CONTACT['email']}" data-cms-href="contact.email_mailto"><span data-cms="contact.email">{CONTACT['email']}</span></a>
      </div>
      <div class="topbar-links">
        <a href="{CONTACT['facebook']}" data-cms-href="contact.facebook" target="_blank" rel="noopener" aria-label="Facebook">{icon_svg('fb')}</a>
        <a href="{CONTACT['instagram']}" data-cms-href="contact.instagram" target="_blank" rel="noopener" aria-label="Instagram">{icon_svg('ig')}</a>
      </div>
    </div>
  </div>
  <nav class="navbar container">
    <a href="{prefix}index.html" class="brand">
      <img class="brand-mark" src="{prefix}images/logo.png" alt="Dr. Dharmalingam Muthiah — Orthopaedic &amp; Trauma Surgery">
      <span class="brand-text">
        <span class="name">Dr. Dharmalingam Muthiah</span>
        <span class="role">Orthopaedic &amp; Trauma Surgeon</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    <div class="nav-links">
      <a href="{prefix}index.html"{cls('home')}>Home</a>
      <a href="{prefix}about.html"{cls('about')}>About Dr</a>
      <div class="has-dropdown{' open' if active=='services' else ''}">
        <a href="{prefix}services.html"{nav_services_active}>Our Services <span class="chevron">{icon_svg('chevron')}</span></a>
        <div class="dropdown" id="nav-services-dropdown" data-prefix="{prefix}" data-current-slug="{current_slug or ''}">
          {services_dropdown_html(current_slug, prefix)}
        </div>
      </div>
      <a href="{prefix}gallery.html"{cls('gallery')}>Gallery</a>
      <a href="{prefix}contact.html"{cls('contact')}>Contact us</a>
      <div class="nav-cta">
        <a href="{prefix}book-consultation.html" class="btn btn-primary"><span>Book Consultation</span></a>
      </div>
    </div>
  </nav>
  <div class="nav-scrim"></div>
</header>
""".strip()


def splash_html(prefix=""):
    return f"""
<div class="splash-screen" id="splash-screen" role="presentation" aria-hidden="true">
  <div class="splash-glow"></div>
  <div class="splash-content">
    <img class="splash-logo" src="{prefix}images/logo.png" alt="Dr. Dharmalingam Muthiah">
    <div class="splash-name">
      <span class="splash-title">Dr. Dharmalingam Muthiah</span>
      <span class="splash-role">Orthopaedic &amp; Trauma Surgeon</span>
    </div>
    <img class="splash-photo" src="{prefix}images/velys-splash.png" alt="Dr. Dharmalingam Muthiah with the VELYS Robotic-Assisted Knee Replacement system">
  </div>
  <div class="splash-tap-hint">Tap anywhere to continue</div>
</div>
""".strip()


def footer_html(prefix=""):
    service_links = "\n".join(
        f'<li><a href="{prefix}services/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES[:6]
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="{prefix}index.html" class="brand">
          <img class="brand-mark" src="{prefix}images/logo.png" alt="Dr. Dharmalingam Muthiah — Orthopaedic &amp; Trauma Surgery">
          <span class="brand-text">
            <span class="name">Dr. Dharmalingam Muthiah</span>
            <span class="role">MBBS (Malaya), FRCS (Edinburgh)</span>
          </span>
        </a>
        <p class="footer-about">Consultant Orthopaedic &amp; Trauma Surgeon at Gleneagles Hospital Kota Kinabalu, providing personalised, evidence-based orthopaedic care for patients across Sabah.</p>
        <div class="footer-social">
          <a href="{CONTACT['facebook']}" data-cms-href="contact.facebook" target="_blank" rel="noopener" aria-label="Facebook">{icon_svg('fb')}</a>
          <a href="{CONTACT['instagram']}" data-cms-href="contact.instagram" target="_blank" rel="noopener" aria-label="Instagram">{icon_svg('ig')}</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="{prefix}about.html">About Dr</a></li>
          <li><a href="{prefix}services.html">Our Services</a></li>
          <li><a href="{prefix}gallery.html">Gallery</a></li>
          <li><a href="{prefix}contact.html">Contact us</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Popular Services</h4>
        <ul id="footer-services-list" data-prefix="{prefix}">
          {service_links}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li id="footer-address-lines">{'<br>'.join(CONTACT['address_lines'])}</li>
          <li><a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener">WhatsApp <span data-cms="contact.whatsapp_display">{CONTACT['whatsapp']}</span></a></li>
          <li><a href="{CONTACT['phone_href']}" data-cms-href="contact.phone_href"><span data-cms="contact.phone_display">{CONTACT['phone']}</span></a></li>
          <li><a href="mailto:{CONTACT['email']}" data-cms-href="contact.email_mailto"><span data-cms="contact.email">{CONTACT['email']}</span></a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Dr. Dharmalingam Muthiah. All Rights Reserved.</span>
      <span>Website Designed &amp; Developed by Click 4 Tech Solutions</span>
    </div>
  </div>
</footer>
<a class="whatsapp-float" href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{icon_svg('whatsapp')}</a>
""".strip()


def page(title, description, active, body, prefix="", extra_head="", show_splash=False, service_slug=None):
    # Body content is authored with root-absolute-looking paths ("/images/x.jpg",
    # "/about.html", etc.) for readability; rewrite them to be relative to this
    # page's location so the same output works both deployed at a domain root
    # (Netlify) and published as a relative-path multi-file bundle (Artifact preview).
    body = body.replace('="/', f'="{prefix}')
    splash_block = splash_html(prefix) if show_splash else ""
    # Runs before first paint so a returning visitor (same browser session) never
    # sees the splash flash on screen — CSS hides it instantly via [data-splash="seen"].
    splash_guard = f"""
<script>
  (function () {{
    try {{
      if (sessionStorage.getItem('dharma_splash_seen')) {{
        document.documentElement.setAttribute('data-splash', 'seen');
      }}
    }} catch (e) {{}}
  }})();
</script>
""".strip() if show_splash else ""
    body_attrs = f' data-service-slug="{service_slug}"' if service_slug else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="{prefix}images/favicon.png">
<link rel="apple-touch-icon" href="{prefix}images/apple-touch-icon.png">
<link rel="manifest" href="{prefix}manifest.json">
<meta name="theme-color" content="#0c1c33">
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', function () {{
    navigator.serviceWorker.register('{prefix}sw.js').catch(function () {{}});
  }});
}}
</script>
<link rel="stylesheet" href="{prefix}css/styles.css">
<link rel="icon" type="image/png" href="{prefix}images/favicon.png">
<link rel="apple-touch-icon" href="{prefix}images/apple-touch-icon.png">
<link rel="manifest" href="{prefix}manifest.json">
<meta name="theme-color" content="#0c1c33">
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', function () {{
    navigator.serviceWorker.register('{prefix}sw.js').catch(function () {{}});
  }});
}}
</script>
<script>window.CMS_PREFIX = "{prefix}";</script>
{splash_guard}
{extra_head}
</head>
<body{body_attrs}>
{splash_block}
{header_html(active, prefix)}
{body}
{footer_html(prefix)}
<script src="{prefix}js/cms-loader.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------

def home_body():
    preview_cards = "\n".join(
        f"""
        <a href="/services/{s['slug']}.html" class="card service-card">
          <div class="icon">{s['icon']}</div>
          <h3>{s['title']}</h3>
          <p>{s['short']}</p>
          <span class="learn">Learn More {icon_svg('arrow')}</span>
        </a>""" for s in [SERVICES_BY_SLUG[slug] for slug in HOME_PREVIEW_SLUGS]
    )

    return f"""
<section class="hero">
  <div class="container">
    <div class="hero-copy">
      <div class="eyebrow" id="hero-eyebrow">Advanced Orthopaedic Technology</div>
      <h1><span id="hero-heading-line1">Robotic-Assisted</span><br><em id="hero-heading-em">Knee Replacement</em></h1>
      <p class="lede" id="hero-lede">Experience the next generation of knee replacement surgery with the VELYS™ Robotic-Assisted Solution. Using advanced precision technology, Dr. Dharmalingam Muthiah delivers personalised treatment designed to improve implant accuracy, minimise pain and help patients return to their active lifestyle sooner.</p>
      <div class="hero-cta">
        <a href="/book-consultation.html" class="btn btn-gold" id="hero-cta-primary">Book Consultation</a>
        <a href="/services/velys-tm-robotic-assisted-robotic-assisted.html" class="btn btn-outline" id="hero-cta-secondary">Learn About VELYS™</a>
      </div>
      <div class="hero-stats">
        <div><b id="hero-stat1-value">13+</b><span id="hero-stat1-label">Areas of Expertise</span></div>
        <div><b id="hero-stat2-value">3</b><span id="hero-stat2-label">Countries of Fellowship Training</span></div>
        <div><b id="hero-stat3-value">Sabah</b><span id="hero-stat3-label">&amp; neighbouring regions served</span></div>
      </div>
    </div>
    <div class="hero-media">
      <img src="/images/doctor-portrait.png" alt="Dr. Dharmalingam Muthiah with the VELYS Robotic-Assisted knee replacement system" id="hero-image">
    </div>
  </div>
</section>

<div class="pill-row">
  <div class="container">
    <div class="pill">{icon_svg('spark')}<span><b>Greater Precision</b><br>Optimised implant positioning for improved alignment and long-term performance.</span></div>
    <div class="pill">{icon_svg('heart')}<span><b>Less Pain</b><br>Minimally invasive techniques preserve healthy tissue and ease recovery.</span></div>
    <div class="pill">{icon_svg('clock')}<span><b>Faster Recovery</b><br>Return to everyday activities sooner, with greater confidence.</span></div>
  </div>
</div>

<section class="band">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow center">What We Treat</div>
      <h2>Comprehensive Orthopaedic Care</h2>
      <p class="lede center">At our clinic, we are committed to providing comprehensive orthopaedic care using modern techniques and evidence-based treatments — restoring mobility, relieving pain and improving quality of life for patients of all ages.</p>
    </div>
    <div class="services-grid" id="home-services-grid">
      {preview_cards}
    </div>
    <div class="center" style="margin-top:40px;">
      <a href="/services.html" class="btn btn-outline-navy">View All 13 Services {icon_svg('arrow')}</a>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="container about-grid">
    <div class="about-media">
      <img src="/images/doctor-portrait.png" alt="Dr. Dharmalingam Muthiah" id="home-about-photo">
    </div>
    <div>
      <div class="eyebrow">About the Specialist</div>
      <h2>Dr. Dharmalingam Muthiah</h2>
      <div class="credentials">
        <span class="credential-chip">MBBS (Malaya)</span>
        <span class="credential-chip">FRCS (Edinburgh)</span>
        <span class="credential-chip">Orthopaedic &amp; Trauma Surgeon</span>
      </div>
      <p id="home-about-para1">Dr. Dharmalingam Muthiah is an Orthopaedic and Trauma Surgeon specialising in Joint Replacement and Sports Reconstructive Surgery. He currently practises at the Orthopaedic &amp; Trauma Surgery Clinic, Gleneagles Hospital Kota Kinabalu, providing orthopaedic and trauma care for patients requiring specialist musculoskeletal treatment.</p>
      <p id="home-about-para2">His clinical practice includes the assessment and management of musculoskeletal disorders, traumatic injuries, degenerative joint conditions, sports-related injuries, hand conditions and musculoskeletal tumours.</p>
      <a href="/about.html" class="btn btn-primary">More About Dr. Dharmalingam {icon_svg('arrow')}</a>
    </div>
  </div>
</section>

<section class="band-navy">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow center">Why Choose Us</div>
      <h2>Committed to Patient-Centred Care</h2>
    </div>
    <ul class="checklist" style="max-width:900px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:16px 40px;">
      <li>{icon_svg('check')} Comprehensive Orthopaedic Care</li>
      <li>{icon_svg('check')} Personalised Treatment Plans</li>
      <li>{icon_svg('check')} Evidence-Based Medical Practice</li>
      <li>{icon_svg('check')} Modern Surgical Techniques</li>
      <li>{icon_svg('check')} Compassionate Patient Care</li>
      <li>{icon_svg('check')} Trusted Orthopaedic Expertise</li>
    </ul>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="cta-strip">
      <div>
        <h2>Need an Orthopaedic Consultation?</h2>
        <p>Our friendly team is ready to assist you with appointments, enquiries and information about our orthopaedic services.</p>
      </div>
      <div class="cta-actions">
        <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp">{icon_svg('whatsapp')} Chat with Us</a>
        <a href="/book-consultation.html" class="btn btn-outline">Book Consultation</a>
      </div>
    </div>
  </div>
</section>
""".strip()


def about_body():
    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <span>About Dr</span></div>
    <div class="eyebrow">About the Specialist</div>
    <h1>Meet Dr. Dharmalingam Muthiah</h1>
    <p class="lede" style="color:#c9d3e3;" id="about-credentials-line">MBBS (Malaya), FRCS (Edinburgh) — Consultant Orthopaedic &amp; Trauma Surgeon</p>
  </div>
</section>

<section class="band">
  <div class="container about-grid">
    <div class="about-media">
      <img src="/images/doctor-portrait.png" alt="Dr. Dharmalingam Muthiah" id="about-photo">
    </div>
    <div>
      <p id="about-bio-para1">Dr. Dharmalingam Muthiah is a highly experienced Orthopaedic and Trauma Surgeon with international training spanning joint replacement, sports reconstruction, trauma, hand surgery and microsurgery. His practice is built around modern, evidence-based orthopaedic care delivered with compassion, precision and personalised treatment.</p>
      <p id="about-bio-para2">He currently serves as Consultant Orthopaedic &amp; Trauma Surgeon at Gleneagles Hospital Kota Kinabalu, providing specialist musculoskeletal care to patients across Sabah and neighbouring regions.</p>
      <p><b id="about-highlight-bold">Every patient deserves personalised care.</b> <span id="about-highlight-rest">His approach is built on careful listening, clear explanations and treatment plans customised to each patient's condition and goals.</span></p>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow center">Training &amp; Qualifications</div>
      <h2>Education, Fellowships &amp; Special Interests</h2>
    </div>
    <div class="card" style="padding:36px;max-width:900px;margin:0 auto;">
      <div class="timeline" id="about-timeline">
        <div class="timeline-item"><div class="place">University of Malaya</div><div>Bachelor of Medicine and Bachelor of Surgery (MBBS)</div></div>
        <div class="timeline-item"><div class="place">Edinburgh, UK</div><div>Fellow of the Royal College of Surgeons (FRCS) &mdash; Orthopaedic &amp; Trauma Surgery Specialist Certification</div></div>
        <div class="timeline-item"><div class="place">Sydney, Australia</div><div>Fellowship training in knee &amp; upper limb surgery</div></div>
        <div class="timeline-item"><div class="place">Basel, Switzerland</div><div>Fellowship training in trauma surgery</div></div>
        <div class="timeline-item"><div class="place">Hand &amp; Microsurgery</div><div>Extensive specialised training throughout his career</div></div>
        <div class="timeline-item"><div class="place">Special Interests</div><div>Arthroscopic Sports &amp; Joint Replacement</div></div>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow center">Clinical Expertise</div>
      <h2>Areas of Practice</h2>
    </div>
    <div class="services-index-grid" id="about-services-grid">
      {"".join(f'''<div class="card services-index-card"><div class="icon">{s["icon"]}</div><div><h3 style="margin-bottom:4px;font-size:1.02rem;">{s["title"]}</h3><p style="margin:0;font-size:.9rem;">{s["short"]}</p></div></div>''' for s in SERVICES)}
    </div>
  </div>
</section>

<section class="band-navy">
  <div class="container" style="max-width:820px;text-align:center;">
    <div class="eyebrow center">Commitment to Patient Care</div>
    <h2>Patient-Centred, Evidence-Based Care</h2>
    <p>Dr. Dharmalingam Muthiah believes in providing patient-centred care through careful clinical assessment, clear communication and evidence-based treatment. He works closely with patients to explain their diagnosis and available treatment options, enabling informed decision-making throughout their care journey.</p>
    <div class="cta-actions" style="justify-content:center;margin-top:24px;">
      <a href="/book-consultation.html" class="btn btn-gold">Book a Consultation</a>
      <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-outline">{icon_svg('whatsapp')} WhatsApp Us</a>
    </div>
  </div>
</section>
""".strip()


def services_index_body():
    cards = "\n".join(
        f"""
        <a href="/services/{s['slug']}.html" class="card services-index-card">
          <div class="icon">{s['icon']}</div>
          <div>
            <h3 style="margin-bottom:6px;">{s['title']}</h3>
            <p style="margin:0;font-size:.92rem;">{s['short']}</p>
          </div>
        </a>""" for s in SERVICES
    )
    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <span>Our Services</span></div>
    <div class="eyebrow">What We Treat</div>
    <h1>Our Services</h1>
    <p class="lede" style="color:#c9d3e3;max-width:680px;">Comprehensive, evidence-based orthopaedic and trauma care — from joint replacement and robotic-assisted surgery to paediatric conditions and non-operative management.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="services-index-grid" id="services-index-grid">
      {cards}
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="cta-strip" style="background:linear-gradient(120deg,var(--navy-800),var(--navy-700));">
      <div>
        <h2>Not sure which service you need?</h2>
        <p>Message us on WhatsApp and our team will help point you in the right direction.</p>
      </div>
      <div class="cta-actions">
        <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp">{icon_svg('whatsapp')} Chat with Us</a>
      </div>
    </div>
  </div>
</section>
""".strip()


def service_detail_body(s):
    includes_html = "\n".join(
        f'<div class="card include-card"><h3>{title}</h3><p>{desc}</p></div>' for title, desc in s["includes"]
    )
    # sidebar: a few related services (excluding current)
    related = [x for x in SERVICES if x["slug"] != s["slug"]][:6]
    sidebar_links = "\n".join(
        f'<a href="/services/{r["slug"]}.html">{r["icon"]} {r["title"]}</a>' for r in related
    )
    intro_html = "\n".join(f"<p>{p}</p>" for p in s["intro"])
    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <a href="/services.html">Our Services</a> / <span id="service-breadcrumb-title">{s['title']}</span></div>
    <div class="icon-lg" id="service-icon">{s['icon']}</div>
    <h1 id="service-title">{s['title']}</h1>
  </div>
</section>

<section class="band">
  <div class="container service-body">
    <div>
      <div id="service-intro">{intro_html}</div>
      <h2 style="margin-top:36px;" id="service-includes-title">{s['includes_title']}</h2>
      <div class="service-includes" id="service-includes">
        {includes_html}
      </div>
      <div class="closing-banner">
        <h3 id="service-closing-title">{s['closing_title']}</h3>
        <p style="margin:0;" id="service-closing-text">{s['closing_text']}</p>
      </div>
    </div>
    <aside>
      <div class="card sidebar-card">
        <h3>Explore Other Services</h3>
        <div class="sidebar-list">
          {sidebar_links}
        </div>
        <a href="/services.html" class="btn btn-outline-navy btn-block" style="margin-top:16px;">View All Services</a>
      </div>
      <div class="card sidebar-card" style="margin-top:20px;position:static;">
        <h3>Book a Consultation</h3>
        <p style="font-size:.9rem;">Speak with Dr. Dharmalingam Muthiah about your condition and treatment options.</p>
        <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp btn-block">{icon_svg('whatsapp')} WhatsApp Us</a>
        <a href="/book-consultation.html" class="btn btn-primary btn-block" style="margin-top:10px;">Book Consultation</a>
      </div>
    </aside>
  </div>
</section>
""".strip()


def gallery_body():
    case_cards = "".join(
        f"""
        <button class="case-card" type="button" data-case="{c['slug']}" aria-label="View {c['title']} photos">
          <div class="case-card-media">
            <img src="/images/gallery/{c['images'][c.get('cover', 0)]}" alt="{c['title']}" loading="lazy">
            <span class="case-count">{icon_svg('image')} {c['count']} photo{'s' if c['count'] != 1 else ''}</span>
          </div>
          <div class="case-card-body">
            <h3>{c['title']}</h3>
            <p>{c['desc']}</p>
          </div>
        </button>"""
        for c in GALLERY_CASES
    )

    video_cards = "".join(
        f"""
        <button class="video-card" type="button" data-video="{v['id']}" aria-label="Play video: {v['title']}">
          <div class="video-card-media">
            <img src="https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg" alt="{v['title']}" loading="lazy">
            <span class="play-btn">{icon_svg('play')}</span>
          </div>
          <div class="video-card-body">
            <h3>{v['title']}</h3>
          </div>
        </button>"""
        for v in VIDEOS
    )

    gallery_data = json.dumps({
        c["slug"]: {"title": c["title"], "images": [f"/images/gallery/{img}" for img in c["images"]]}
        for c in GALLERY_CASES
    })
    video_data = json.dumps([{"id": v["id"], "title": v["title"]} for v in VIDEOS])

    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <span>Gallery</span></div>
    <div class="eyebrow">Case Highlights</div>
    <h1>Gallery</h1>
    <p class="lede" style="color:#c9d3e3;">A selection of real clinical cases and procedures, plus video case highlights from Dr. Dharmalingam's own YouTube channel.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="gallery-tabs" role="tablist">
      <button class="gallery-tab active" type="button" data-tab="photos" role="tab" aria-selected="true">{icon_svg('image')} Photo Gallery</button>
      <button class="gallery-tab" type="button" data-tab="videos" role="tab" aria-selected="false">{icon_svg('play')} Video Gallery</button>
    </div>

    <div class="gallery-panel" data-panel="photos">
      <div class="case-grid" id="gallery-case-grid">
        {case_cards}
      </div>
    </div>

    <div class="gallery-panel" data-panel="videos" hidden>
      <div class="video-grid" id="gallery-video-grid">
        {video_cards}
      </div>
      <p class="video-note">More clinical videos are added regularly on our <a href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener">YouTube channel</a> — subscribe to stay updated.</p>
    </div>

    <div class="card band-cream" style="margin-top:40px;padding:36px;text-align:center;">
      <h3>Want to see more?</h3>
      <p>More case studies and patient outcomes are available on request.</p>
      <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp">{icon_svg('whatsapp')} Ask Us on WhatsApp</a>
    </div>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden>
  <div class="lightbox-backdrop" data-close="1"></div>
  <div class="lightbox-inner">
    <button class="lightbox-close" type="button" data-close="1" aria-label="Close">{icon_svg('close')}</button>
    <button class="lightbox-prev" type="button" aria-label="Previous photo">{icon_svg('chevron')}</button>
    <img class="lightbox-img" alt="">
    <button class="lightbox-next" type="button" aria-label="Next photo">{icon_svg('chevron')}</button>
    <div class="lightbox-caption">
      <span class="lightbox-title"></span>
      <span class="lightbox-count"></span>
    </div>
  </div>
</div>

<div class="lightbox" id="video-lightbox" hidden>
  <div class="lightbox-backdrop" data-close="1"></div>
  <div class="lightbox-inner">
    <button class="lightbox-close" type="button" data-close="1" aria-label="Close">{icon_svg('close')}</button>
    <button class="lightbox-prev" type="button" aria-label="Previous video">{icon_svg('chevron')}</button>
    <div class="lightbox-video-wrap">
      <iframe id="video-lightbox-iframe" src="" title="Video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      <video id="video-lightbox-native" controls playsinline hidden></video>
    </div>
    <button class="lightbox-next" type="button" aria-label="Next video">{icon_svg('chevron')}</button>
    <div class="lightbox-caption">
      <span class="lightbox-title" id="video-lightbox-title"></span>
      <span class="lightbox-count" id="video-lightbox-count"></span>
    </div>
  </div>
</div>

<script id="gallery-data" type="application/json">{gallery_data}</script>
<script id="video-data" type="application/json">{video_data}</script>
""".strip()


def contact_body():
    hours_html = "".join(f"<p><b>{d}</b><br>{h}</p>" for d, h in CONTACT["hours"])
    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <span>Contact us</span></div>
    <div class="eyebrow">Get In Touch</div>
    <h1>Contact Us</h1>
    <p class="lede" style="color:#c9d3e3;">Please feel free to share your enquiry with us, and we will respond as quickly as possible.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="info-grid" style="margin-bottom:48px;">
      <div class="card info-card">
        <div class="icon">{icon_svg('pin')}</div>
        <h3>Clinic Address</h3>
        <p>Gleneagles Hospital Kota Kinabalu<br><span id="contact-address-lines">{'<br>'.join(CONTACT['address_lines'])}</span></p>
      </div>
      <div class="card info-card">
        <div class="icon">{icon_svg('phone')}</div>
        <h3>Phone</h3>
        <p><a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener">WhatsApp: {CONTACT['whatsapp']}</a></p>
        <p><a href="{CONTACT['phone_href']}" data-cms-href="contact.phone_href">Clinic: {CONTACT['phone']}</a></p>
      </div>
      <div class="card info-card">
        <div class="icon">{icon_svg('mail')}</div>
        <h3>Email</h3>
        <p><a href="mailto:{CONTACT['email']}" data-cms-href="contact.email_mailto">{CONTACT['email']}</a></p>
      </div>
      <div class="card info-card">
        <div class="icon">{icon_svg('clock')}</div>
        <h3>Business Hours</h3>
        <div id="contact-hours">{hours_html}</div>
      </div>
    </div>

    <div class="service-body">
      <div class="card" style="padding:36px;">
        <h2>Send an Enquiry</h2>
        <p>Drop us your enquiry here and we will get back to you as soon as possible.</p>
        <form id="contact-form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="contact">
          <p style="position:absolute;left:-9999px;" aria-hidden="true"><label>Leave this field blank: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div class="form-grid">
            <div><label for="fname">First name *</label><input id="fname" name="fname" required></div>
            <div><label for="lname">Last name *</label><input id="lname" name="lname" required></div>
            <div><label for="email">Email address *</label><input id="email" type="email" name="email" required></div>
            <div><label for="phone">Phone Number</label><input id="phone" name="phone" placeholder="+60"></div>
            <div class="full"><label for="message">Enter your enquiry *</label><textarea id="message" name="message" required></textarea></div>
          </div>
          <button type="submit" class="btn btn-primary" style="margin-top:18px;">Submit</button>
        </form>
      </div>
      <aside class="card sidebar-card">
        <h3>Prefer WhatsApp?</h3>
        <p style="font-size:.9rem;">Our team typically responds fastest on WhatsApp for appointments and urgent enquiries.</p>
        <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp btn-block">{icon_svg('whatsapp')} Chat on WhatsApp</a>
        <div style="margin-top:22px;border-top:1px solid var(--line);padding-top:18px;">
          <h3>Find Us</h3>
          <p style="font-size:.9rem;">Gleneagles Hospital Kota Kinabalu, Suite 02-06, Level 6, Riverson@Sembulan, Off Coastal Highway, 88100 Kota Kinabalu, Sabah.</p>
          <a href="https://www.google.com/maps/search/?api=1&query=Gleneagles+Hospital+Kota+Kinabalu" target="_blank" rel="noopener" class="btn btn-outline-navy btn-block">Open in Google Maps</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<div class="form-modal" id="form-modal" hidden>
  <div class="form-modal-backdrop" data-close="1"></div>
  <div class="form-modal-inner" role="dialog" aria-modal="true" aria-labelledby="form-modal-title">
    <button class="form-modal-close" type="button" data-close="1" aria-label="Close">{icon_svg('close')}</button>
    <img class="form-modal-logo" src="/images/logo.png" alt="Dr. Dharmalingam Muthiah">
    <h3 class="form-modal-title" id="form-modal-title"></h3>
    <p class="form-modal-message"></p>
    <button class="btn btn-primary form-modal-ok" type="button" data-close="1">Close</button>
  </div>
</div>
""".strip()


def booking_body():
    return f"""
<section class="service-hero">
  <div class="container">
    <div class="breadcrumb"><a href="/index.html">Home</a> / <span>Book Consultation</span></div>
    <div class="eyebrow">Request an Appointment</div>
    <h1>Book a Consultation</h1>
    <p class="lede" style="color:#c9d3e3;">Tell us a little about the patient and pick a preferred date and time — our clinic team will confirm your appointment shortly after.</p>
  </div>
</section>

<section class="band">
  <div class="container" style="max-width:820px;">
    <div class="booking-note">
      <strong>Please note:</strong> this is a booking request, not a confirmed appointment. Our clinic team will contact you to finalise the exact date and time based on Dr. Dharmalingam Muthiah's availability.
    </div>

    <div class="card" style="padding:36px;">
      <form id="booking-form" name="booking" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="booking">
        <p style="position:absolute;left:-9999px;" aria-hidden="true"><label>Leave this field blank: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

        <h2 class="booking-section-title"><span>1</span> Patient's Details</h2>
        <div class="form-grid">
          <div>
            <label for="salutation">Salutation *</label>
            <select id="salutation" name="salutation" required>
              <option value="" disabled selected>Please select</option>
              <option>Mr</option>
              <option>Mrs</option>
              <option>Ms</option>
              <option>Madam</option>
              <option>Miss</option>
              <option>Dr</option>
            </select>
          </div>
          <div><label for="patient-name">Patient's Name *</label><input id="patient-name" name="patient_name" required></div>
          <div><label for="dob">Date of Birth *</label><input id="dob" type="date" name="date_of_birth" required></div>
          <div>
            <label for="nric">NRIC / Passport No *</label>
            <input id="nric" name="nric_passport" placeholder="e.g. 901231-14-5678 or passport no." maxlength="20" autocomplete="off" required>
            <p id="nric-error" class="booking-error" hidden>Please enter a complete NRIC (xxxxxx-xx-xxxx) or a passport number.</p>
          </div>
          <div><label for="phone">Contact Number *</label><input id="phone" name="phone" placeholder="+60" required></div>
          <div><label for="patient-email">Email *</label><input id="patient-email" type="email" name="email" required></div>
        </div>

        <h2 class="booking-section-title"><span>2</span> Select Your Date</h2>
        <p class="booking-hint">Clinic is open Monday–Saturday. Please request an appointment at least a day in advance.</p>
        <div class="form-grid">
          <div class="full">
            <label for="apt-date">Preferred Date *</label>
            <input id="apt-date" type="date" name="preferred_date" required>
            <p id="date-error" class="booking-error" hidden>We're closed on Sundays — please choose a date from Monday to Saturday.</p>
          </div>
        </div>

        <h2 class="booking-section-title"><span>3</span> Select Your Time</h2>
        <p class="booking-hint" id="time-hint">Pick a date above to see available time slots.</p>
        <div class="time-slot-grid" id="time-slot-grid"></div>
        <input type="hidden" id="apt-time" name="preferred_time" required>

        <button type="submit" class="btn btn-primary" style="margin-top:28px;">Request Appointment</button>
      </form>
    </div>

    <div class="card band-cream" style="margin-top:28px;padding:28px 30px;text-align:center;">
      <h3 style="margin-bottom:6px;">Prefer to book by WhatsApp instead?</h3>
      <p style="font-size:.9rem;margin-bottom:16px;">Message our team directly for appointments and urgent enquiries.</p>
      <a href="{CONTACT['whatsapp_href']}" data-cms-href="contact.whatsapp_href" target="_blank" rel="noopener" class="btn btn-whatsapp">{icon_svg('whatsapp')} Chat on WhatsApp</a>
    </div>
  </div>
</section>

<div class="form-modal" id="form-modal" hidden>
  <div class="form-modal-backdrop" data-close="1"></div>
  <div class="form-modal-inner" role="dialog" aria-modal="true" aria-labelledby="form-modal-title">
    <button class="form-modal-close" type="button" data-close="1" aria-label="Close">{icon_svg('close')}</button>
    <img class="form-modal-logo" src="/images/logo.png" alt="Dr. Dharmalingam Muthiah">
    <h3 class="form-modal-title" id="form-modal-title"></h3>
    <p class="form-modal-message"></p>
    <button class="btn btn-primary form-modal-ok" type="button" data-close="1">Close</button>
  </div>
</div>

<script id="booking-slots-data" type="application/json">{json.dumps(BOOKING_SLOTS)}</script>
""".strip()

# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def main():
    write("index.html", page(
        "Dr. Dharmalingam Muthiah | Orthopaedic & Trauma Surgery, Kota Kinabalu",
        "Consultant Orthopaedic & Trauma Surgeon at Gleneagles Hospital Kota Kinabalu — joint replacement, robotic-assisted knee surgery, sports reconstruction, trauma & hand surgery.",
        "home", home_body(), show_splash=True,
    ))
    write("about.html", page(
        "About Dr. Dharmalingam Muthiah | Orthopaedic & Trauma Surgeon",
        "MBBS (Malaya), FRCS (Edinburgh) — training in Sydney, Basel and beyond. Consultant Orthopaedic & Trauma Surgeon, Gleneagles Hospital Kota Kinabalu.",
        "about", about_body(),
    ))
    write("services.html", page(
        "Our Services | Dr. Dharmalingam Muthiah Orthopaedic & Trauma Surgery",
        "13 areas of orthopaedic expertise — joint replacement, robotic-assisted knee surgery, trauma, hand & ankle, paediatric orthopaedics, tumours and more.",
        "services", services_index_body(),
    ))
    write("gallery.html", page(
        "Gallery | Dr. Dharmalingam Muthiah",
        "Clinical case highlights from Dr. Dharmalingam Muthiah's orthopaedic and trauma surgery practice.",
        "gallery", gallery_body(),
    ))
    write("contact.html", page(
        "Contact Us | Dr. Dharmalingam Muthiah",
        "Contact Dr. Dharmalingam Muthiah's clinic at Gleneagles Hospital Kota Kinabalu — WhatsApp, phone, email, address and business hours.",
        "contact", contact_body(),
    ))
    write("book-consultation.html", page(
        "Book a Consultation | Dr. Dharmalingam Muthiah",
        "Request a consultation with Dr. Dharmalingam Muthiah at Gleneagles Hospital Kota Kinabalu — pick a preferred date and time and our team will confirm.",
        "", booking_body(),
    ))

    for s in SERVICES:
        write(f"services/{s['slug']}.html", page(
            f"{s['title']} | Dr. Dharmalingam Muthiah",
            s["short"],
            "services", service_detail_body(s), prefix="../", extra_head="", service_slug=s["slug"],
        ))

    print(f"\nDone. Generated {6 + len(SERVICES)} pages.")


if __name__ == "__main__":
    main()
