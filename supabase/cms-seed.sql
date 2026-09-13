-- dharmaortho.my — CMS seed data
-- Run AFTER cms-schema.sql, once, in the Supabase SQL Editor.
-- Populates the CMS with the site's REAL current content, transcribed directly
-- from build.py, so the CMS starts populated and nothing visibly changes on
-- the live site until you actually edit something in the dashboard.
-- Safe to re-run: every insert is ON CONFLICT DO UPDATE (upsert) or DO NOTHING.

-- Hero (home page)
insert into cms_hero (id, eyebrow, heading_line1, heading_em, lede, cta_primary_label, cta_primary_href, cta_secondary_label, cta_secondary_href, stat1_value, stat1_label, stat2_value, stat2_label, stat3_value, stat3_label, hero_image_url)
values (1, 'Advanced Orthopaedic Technology', 'Robotic-Assisted', 'Knee Replacement',
  'Experience the next generation of knee replacement surgery with the VELYS™ Robotic-Assisted Solution. Using advanced precision technology, Dr. Dharmalingam Muthiah delivers personalised treatment designed to improve implant accuracy, minimise pain and help patients return to their active lifestyle sooner.',
  'Book Consultation', '/book-consultation.html',
  'Learn About VELYS™', '/services/velys-tm-robotic-assisted-robotic-assisted.html',
  '13+', 'Areas of Expertise',
  '3', 'Countries of Fellowship Training',
  'Sabah', '& neighbouring regions served',
  '/images/doctor-portrait.png')
on conflict (id) do update set
  eyebrow=excluded.eyebrow, heading_line1=excluded.heading_line1, heading_em=excluded.heading_em, lede=excluded.lede,
  cta_primary_label=excluded.cta_primary_label, cta_primary_href=excluded.cta_primary_href,
  cta_secondary_label=excluded.cta_secondary_label, cta_secondary_href=excluded.cta_secondary_href,
  stat1_value=excluded.stat1_value, stat1_label=excluded.stat1_label,
  stat2_value=excluded.stat2_value, stat2_label=excluded.stat2_label,
  stat3_value=excluded.stat3_value, stat3_label=excluded.stat3_label,
  hero_image_url=excluded.hero_image_url;

-- About (About Dr page + Home mini-about)
insert into cms_about (id, credentials_line, bio_para1, bio_para2, bio_highlight_bold, bio_highlight_rest, home_bio_para1, home_bio_para2, photo_url)
values (1,
  'MBBS (Malaya), FRCS (Edinburgh) — Consultant Orthopaedic & Trauma Surgeon',
  'Dr. Dharmalingam Muthiah is a highly experienced Orthopaedic and Trauma Surgeon with international training spanning joint replacement, sports reconstruction, trauma, hand surgery and microsurgery. His practice is built around modern, evidence-based orthopaedic care delivered with compassion, precision and personalised treatment.',
  'He currently serves as Consultant Orthopaedic & Trauma Surgeon at Gleneagles Hospital Kota Kinabalu, providing specialist musculoskeletal care to patients across Sabah and neighbouring regions.',
  'Every patient deserves personalised care.',
  'His approach is built on careful listening, clear explanations and treatment plans customised to each patient''s condition and goals.',
  'Dr. Dharmalingam Muthiah is an Orthopaedic and Trauma Surgeon specialising in Joint Replacement and Sports Reconstructive Surgery. He currently practises at the Orthopaedic & Trauma Surgery Clinic, Gleneagles Hospital Kota Kinabalu, providing orthopaedic and trauma care for patients requiring specialist musculoskeletal treatment.',
  'His clinical practice includes the assessment and management of musculoskeletal disorders, traumatic injuries, degenerative joint conditions, sports-related injuries, hand conditions and musculoskeletal tumours.',
  '/images/doctor-portrait.png')
on conflict (id) do update set
  credentials_line=excluded.credentials_line, bio_para1=excluded.bio_para1, bio_para2=excluded.bio_para2,
  bio_highlight_bold=excluded.bio_highlight_bold, bio_highlight_rest=excluded.bio_highlight_rest,
  home_bio_para1=excluded.home_bio_para1, home_bio_para2=excluded.home_bio_para2, photo_url=excluded.photo_url;

-- Timeline (About Dr page — Education, Fellowships & Special Interests)
delete from cms_timeline_items;
insert into cms_timeline_items (place, description, sort_order) values ('University of Malaya', 'Bachelor of Medicine and Bachelor of Surgery (MBBS)', 0);
insert into cms_timeline_items (place, description, sort_order) values ('Edinburgh, UK', 'Fellow of the Royal College of Surgeons (FRCS) — Orthopaedic & Trauma Surgery Specialist Certification', 1);
insert into cms_timeline_items (place, description, sort_order) values ('Sydney, Australia', 'Fellowship training in knee & upper limb surgery', 2);
insert into cms_timeline_items (place, description, sort_order) values ('Basel, Switzerland', 'Fellowship training in trauma surgery', 3);
insert into cms_timeline_items (place, description, sort_order) values ('Hand & Microsurgery', 'Extensive specialised training throughout his career', 4);
insert into cms_timeline_items (place, description, sort_order) values ('Special Interests', 'Arthroscopic Sports & Joint Replacement', 5);

-- Services (13 areas of practice)
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('orthopedic-and-trauma-surgery', '🩺', 'Orthopaedic Trauma Surgery', 'Expert surgical management of fractures and traumatic musculoskeletal injuries.', '["Traumatic injuries require prompt assessment and expert orthopaedic care to minimise complications and restore function. We specialise in the management of fractures and complex musculoskeletal injuries resulting from road traffic accidents, falls, sports injuries and workplace trauma.", "Every injury is unique. Our treatment approach focuses on accurate diagnosis, timely intervention and personalised rehabilitation plans to help patients recover safely, regain mobility and return to their normal daily activities as quickly as possible."]'::jsonb,
  'Our Orthopaedic Trauma Services Include', '[{"title": "Simple & Complex Fracture Fixation", "desc": "Surgical and non-surgical management of simple, displaced and complex fractures using modern fixation techniques to promote optimal bone healing and restore stability."}, {"title": "Bone Reconstruction", "desc": "Comprehensive treatment for complex bone injuries requiring reconstruction to restore alignment, strength and function following severe trauma."}, {"title": "Trauma-Related Soft Tissue Injuries", "desc": "Assessment and treatment of ligament, tendon, muscle and soft tissue injuries associated with fractures and traumatic accidents to support complete recovery."}, {"title": "Post-Traumatic Rehabilitation Planning", "desc": "Individualised rehabilitation programmes designed to improve strength, mobility and function while reducing recovery time and supporting a safe return to everyday activities."}]'::jsonb, 'Restoring Function. Rebuilding Lives.', 'Our goal is to restore movement, reduce pain and help patients recover confidently following traumatic injuries. By combining advanced orthopaedic techniques with comprehensive rehabilitation planning, we strive to achieve faster healing, safer recovery and the best possible long-term outcomes for every patient.',
  true, 0)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('joint-replacement-services', '🦿', 'Joint Replacement Surgery', 'Advanced joint replacement procedures to restore function and mobility.', '["Joint replacement surgery is an effective solution for patients experiencing persistent joint pain, stiffness and reduced mobility caused by advanced arthritis, injury or degenerative joint conditions. When conservative treatments are no longer effective, joint replacement can help restore movement, relieve pain and significantly improve quality of life.", "We provide comprehensive assessment and personalised treatment plans using modern surgical techniques and evidence-based care. Every patient receives an individualised approach aimed at achieving the best possible functional outcome and a faster return to daily activities."]'::jsonb,
  'Our Joint Replacement Services Include', '[{"title": "Hip Replacement Surgery", "desc": "Advanced surgical treatment for damaged hip joints to relieve chronic pain, improve mobility and restore normal function."}, {"title": "Knee Replacement Surgery", "desc": "Partial and total knee replacement procedures designed to reduce pain, improve joint stability and help patients regain an active lifestyle."}, {"title": "Revision Joint Replacement", "desc": "Assessment and management of previously replaced joints requiring further surgery due to wear, loosening, infection or implant-related complications."}, {"title": "Preoperative Assessment & Planning", "desc": "Thorough evaluation, diagnostic imaging and personalised surgical planning to ensure the most appropriate treatment for each patient''s condition and lifestyle."}, {"title": "Postoperative Rehabilitation", "desc": "Comprehensive rehabilitation programmes focused on restoring strength, flexibility, balance and confidence following joint replacement surgery."}]'::jsonb, 'Helping You Move Comfortably Again', 'Our goal is to relieve pain, restore joint function and improve your quality of life through advanced joint replacement surgery and personalised rehabilitation. From your initial consultation through recovery, we are committed to providing compassionate care and supporting you every step of your journey towards renewed mobility and independence.',
  true, 1)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('general-orthopaedic-services', '🦴', 'General Orthopaedic Services', 'Comprehensive diagnosis and treatment for bone, joint, muscle, tendon and ligament conditions.', '["From common bone and joint conditions to complex musculoskeletal disorders, our practice provides comprehensive orthopaedic assessment, accurate diagnosis and personalised treatment plans tailored to each patient''s individual needs and lifestyle.", "We focus on relieving pain, restoring mobility, improving function and helping patients return to their daily activities safely and confidently through evidence-based orthopaedic care."]'::jsonb,
  'Our General Orthopaedic Services Include', '[{"title": "Joint Pain & Arthritis", "desc": "Assessment and treatment for osteoarthritis, inflammatory arthritis and chronic joint pain affecting the shoulder, hip, knee, elbow, wrist and ankle."}, {"title": "Bone & Muscle Disorders", "desc": "Diagnosis and management of musculoskeletal conditions involving bones, muscles and connective tissues."}, {"title": "Ligament & Tendon Injuries", "desc": "Comprehensive care for sprains, strains, tendon tears and ligament injuries using both non-surgical and surgical treatment options."}, {"title": "Sports-Related Injuries", "desc": "Expert management of acute and overuse injuries to help athletes and active individuals recover and return to peak performance."}, {"title": "Fractures & Trauma", "desc": "Assessment, fracture management and follow-up care for simple and complex bone injuries resulting from accidents or falls."}, {"title": "Degenerative Musculoskeletal Conditions", "desc": "Long-term treatment strategies for age-related joint degeneration, chronic pain and reduced mobility."}]'::jsonb, 'Personalised Orthopaedic Care', 'Every patient receives an individualised treatment plan that may include lifestyle modification, medication, physiotherapy, rehabilitation, minimally invasive procedures or surgery when required. Our goal is to deliver compassionate, evidence-based orthopaedic care that supports long-term joint health, restores mobility and improves overall quality of life.',
  true, 2)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('hip-replacement', '🦵', 'Hip Replacement', 'Modern hip replacement solutions tailored to each patient''s needs.', '["Hip replacement is a highly successful procedure designed to relieve chronic hip pain, restore movement and improve quality of life for patients with severe arthritis, fractures and degenerative hip conditions.", "Using contemporary surgical techniques, comprehensive preoperative planning and structured rehabilitation support, we provide a personalised treatment journey designed around each patient''s condition and goals throughout recovery."]'::jsonb,
  'Benefits of Hip Replacement', '[{"title": "Pain Relief", "desc": "Significant relief from chronic pain caused by arthritis and other degenerative hip diseases."}, {"title": "Enhanced Mobility", "desc": "Improved mobility and flexibility, making daily tasks easier and more comfortable."}, {"title": "Improved Quality of Life", "desc": "A renewed sense of independence and the ability to enjoy everyday activities again."}, {"title": "Long-Lasting Results", "desc": "Durable outcomes with modern implants designed for long-term performance."}]'::jsonb, 'A Personalised Path to Recovery', 'Every hip replacement journey is tailored to the individual — from detailed preoperative planning through to structured postoperative rehabilitation — helping patients return to a comfortable, active and independent lifestyle with confidence.',
  true, 3)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('velys-tm-robotic-assisted-robotic-assisted', '🤖', 'VELYS™ Robotic-Assisted Knee Replacement', 'VELYS™ robotic-assisted technology for enhanced surgical precision.', '["Experience the next generation of knee replacement surgery with the VELYS\u2122 Robotic-Assisted Solution. Combining advanced robotic technology with surgical expertise, Dr. Dharmalingam Muthiah provides a personalised approach to total knee replacement, helping patients achieve improved implant positioning, enhanced joint function and greater confidence in their recovery.", "Every knee is unique. The VELYS\u2122 system allows precise planning and real-time surgical guidance tailored to your individual anatomy \u2014 supporting accurate implant placement, reduced discomfort, optimised movement and improved long-term outcomes while enabling a faster return to everyday activities."]'::jsonb,
  'Benefits of VELYS™ Robotic-Assisted Knee Replacement', '[{"title": "Greater Precision", "desc": "Advanced robotic guidance assists with highly accurate implant positioning and alignment, helping to optimise joint balance, improve movement and support long-term implant performance."}, {"title": "Less Pain", "desc": "Minimally invasive surgical techniques help preserve healthy bone and surrounding soft tissues, reducing postoperative discomfort and promoting a smoother healing process."}, {"title": "Faster Recovery", "desc": "Many patients are able to regain mobility sooner, return to their daily activities with greater confidence and experience an improved quality of life following surgery."}]'::jsonb, 'Regain Your Active Lifestyle', 'If knee arthritis is affecting your mobility, comfort and independence, VELYS™ Robotic-Assisted Knee Replacement offers an advanced treatment option focused on precision, comfort and long-term function — helping you move more naturally and return to the activities you enjoy with renewed confidence.',
  true, 4)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('arthroscopic-sports-surgery', '🏃', 'Arthroscopic (Keyhole) Sports Surgery', 'Minimally invasive treatment for sports injuries and ligament reconstruction.', '["Arthroscopy, commonly known as keyhole surgery, is a minimally invasive surgical technique used to diagnose and treat a wide range of joint conditions through small incisions. Using a tiny camera and specialised instruments, arthroscopic surgery allows precise treatment while minimising damage to surrounding tissues.", "Compared to conventional open surgery, arthroscopy generally offers less postoperative pain, smaller scars, reduced risk of complications and a faster recovery \u2014 particularly beneficial for active individuals and athletes who wish to return safely to work, sports and their everyday activities."]'::jsonb,
  'Arthroscopic Procedures We Perform', '[{"title": "Shoulder Arthroscopy", "desc": "Minimally invasive treatment for rotator cuff tears, shoulder instability, frozen shoulder and labral injuries, helping restore strength, stability and range of motion."}, {"title": "Elbow Arthroscopy", "desc": "Management of tennis elbow, ligament injuries, loose bodies and elbow stiffness, with the aim of relieving pain and improving joint function."}, {"title": "Wrist Arthroscopy", "desc": "Treatment for ligament injuries, cartilage damage, chronic wrist pain and sports-related wrist injuries, allowing accurate diagnosis and targeted treatment."}, {"title": "Hip Arthroscopy", "desc": "Surgical management of hip impingement, labral tears and hip instability, helping preserve the natural hip joint while improving movement and reducing discomfort."}, {"title": "Knee Arthroscopy", "desc": "Treatment of meniscus tears, ACL and ligament injuries, cartilage damage, sports injuries and loose bodies, supporting faster recovery and a safe return to physical activity."}]'::jsonb, 'Minimally Invasive. Faster Recovery.', 'Our goal is to restore joint function while minimising pain and recovery time through advanced arthroscopic techniques. Every patient receives a personalised treatment and rehabilitation plan tailored to their condition, activity level and recovery goals.',
  true, 5)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('hand-ankle-surgery', '✋', 'Hand & Ankle Surgery', 'Specialist care for hand, wrist, foot and ankle conditions.', '["Conditions affecting the hand and ankle can significantly impact mobility, strength and everyday activities. Whether caused by injury, repetitive strain, sports participation or age-related degeneration, these conditions require specialised assessment and treatment to restore normal function and reduce pain.", "We provide comprehensive surgical and non-surgical management for a wide range of hand and ankle conditions, using modern orthopaedic techniques and personalised rehabilitation programmes to help patients regain movement and return confidently to work, sports and daily life."]'::jsonb,
  'Conditions We Treat', '[{"title": "Tendon Injuries", "desc": "Expert management of tendon tears, ruptures and overuse injuries affecting the hand, wrist, ankle and foot to restore strength, flexibility and normal movement."}, {"title": "Ligament Injuries", "desc": "Treatment for ligament sprains, instability and complete ligament tears using both conservative care and advanced surgical reconstruction when required."}, {"title": "Fractures", "desc": "Comprehensive assessment and treatment of simple and complex fractures involving the hand, fingers, wrist, ankle and foot to promote proper healing and restore function."}, {"title": "Nerve Compression Syndromes", "desc": "Diagnosis and treatment of nerve compression conditions, including carpal tunnel syndrome and other peripheral nerve disorders that cause pain, numbness and weakness."}, {"title": "Degenerative Conditions", "desc": "Management of arthritis and other degenerative disorders affecting the hand and ankle to relieve pain, improve joint mobility and maintain function."}, {"title": "Sports Injuries", "desc": "Treatment of acute and chronic sports-related injuries involving the hand, wrist, ankle and foot, with a focus on safe recovery and return to sporting activities."}]'::jsonb, 'Restoring Movement. Strengthening Recovery.', 'Our approach combines accurate diagnosis, advanced surgical expertise and personalised rehabilitation to achieve the best possible outcomes — helping every patient regain strength, restore function and return to an active, independent lifestyle.',
  true, 6)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('soft-tissue-tumours', '🔬', 'Soft Tissue Tumours', 'Diagnosis and management of benign and malignant soft tissue tumours.', '["Soft tissue lumps and tumours can develop in muscles, fat, tendons, ligaments and other connective tissues throughout the body. While many soft tissue lumps are benign, some require further investigation to determine their nature and ensure appropriate treatment.", "We provide comprehensive assessment and management of soft tissue tumours using a systematic approach that includes clinical evaluation, appropriate investigations and personalised treatment planning, with a priority on accurate diagnosis and safe, effective care."]'::jsonb,
  'Our Soft Tissue Tumour Services Include', '[{"title": "Clinical Evaluation", "desc": "A thorough consultation and physical examination to assess the size, location, characteristics and symptoms of soft tissue lumps, helping determine the most appropriate next steps."}, {"title": "Diagnostic Assessment", "desc": "Appropriate diagnostic investigations, including imaging studies and other necessary assessments, to accurately identify the nature of the soft tissue tumour and guide treatment planning."}, {"title": "Surgical Removal of Suitable Soft Tissue Tumours", "desc": "Careful surgical excision of suitable benign and selected soft tissue tumours using techniques that prioritise complete removal, functional preservation and optimal healing."}, {"title": "Ongoing Follow-Up Care", "desc": "Regular postoperative reviews and long-term monitoring to assess healing, recovery and detect any recurrence or concerns, ensuring continued patient wellbeing."}]'::jsonb, 'Early Assessment Leads to Better Outcomes', 'Early evaluation of soft tissue lumps is important to determine whether they require observation, further investigation or surgical treatment. We are committed to providing timely diagnosis, personalised treatment and comprehensive follow-up care.',
  false, 7)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('musculoskeletal-infections', '🦠', 'Musculoskeletal Infections', 'Comprehensive treatment for bone, joint and soft tissue infections.', '["Musculoskeletal infections involving the bones, joints and surrounding soft tissues require early diagnosis and prompt treatment to prevent long-term complications. If left untreated, these infections may lead to chronic pain, joint damage, reduced mobility and permanent loss of function.", "We provide comprehensive assessment and management for a wide range of musculoskeletal infections, combining accurate diagnosis, evidence-based treatment and personalised rehabilitation to help patients recover safely."]'::jsonb,
  'Our Musculoskeletal Infection Services Include', '[{"title": "Clinical Assessment", "desc": "Comprehensive evaluation of symptoms, medical history and physical examination to identify signs of bone, joint or soft tissue infection and determine the severity of the condition."}, {"title": "Diagnostic Investigations", "desc": "Appropriate laboratory tests, imaging studies and other diagnostic investigations are performed to accurately identify the source of infection and guide the most effective treatment plan."}, {"title": "Medical & Surgical Management", "desc": "Treatment may include antibiotic therapy, surgical drainage, removal of infected tissue or other orthopaedic procedures where necessary to eliminate infection and preserve joint and bone function."}, {"title": "Infection Control & Rehabilitation", "desc": "Ongoing monitoring, infection control measures and structured rehabilitation programmes are provided to support recovery, restore mobility and reduce the risk of recurrence."}]'::jsonb, 'Prompt Diagnosis. Effective Treatment. Lasting Recovery.', 'Early diagnosis and appropriate treatment are essential for achieving the best possible outcomes in musculoskeletal infections. Our approach focuses on controlling infection, preserving healthy bone and joint function, and helping patients return to their normal daily activities with confidence.',
  true, 8)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('specialist-assessment-management', '📋', 'Specialist Assessment & Management', 'Personalised consultations, diagnosis and long-term orthopaedic management.', '["Not every orthopaedic condition requires surgery. We provide comprehensive specialist assessment and personalised non-operative management for a wide range of musculoskeletal disorders, helping patients achieve pain relief, improved mobility and a better quality of life through evidence-based treatment.", "Every patient receives a thorough clinical evaluation, supported by appropriate investigations where necessary, to identify the underlying cause of their symptoms and develop an individualised treatment plan that avoids unnecessary surgery whenever possible."]'::jsonb,
  'Comprehensive Orthopaedic Assessment', '[{"title": "Clinical Evaluation", "desc": "Detailed assessment of your symptoms, medical history and physical examination to accurately diagnose orthopaedic conditions and recommend the most appropriate treatment options."}, {"title": "Non-Operative Management", "desc": "Personalised treatment plans may include medication, physiotherapy, lifestyle modification, rehabilitation and other conservative treatment approaches aimed at relieving pain and restoring function."}, {"title": "Neck & Back Pain (Spinal Disorders)", "desc": "Assessment and management of acute and chronic neck and back pain, sciatica and degenerative spinal conditions affecting the cervical, thoracic and lumbar spine."}, {"title": "Referral for Complex Spinal Surgery", "desc": "Patients requiring specialised spinal procedures or complex spinal surgery will be referred to experienced spine specialists to ensure they receive the most appropriate expert care."}]'::jsonb, 'Expert Care. Personalised Treatment.', 'Our goal is to provide accurate diagnosis, effective non-operative treatment and clear guidance to help patients manage orthopaedic conditions with confidence — focusing on conservative care whenever surgery is not required.',
  true, 9)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('paediatric-orthopaedic-disorders', '👶', 'Paediatric Orthopaedic Disorders', 'Assessment and management of orthopaedic conditions in growing children.', '["Children''s bones, joints and muscles are continually growing and developing, making paediatric orthopaedic conditions different from those seen in adults. Early assessment is essential to identify developmental problems, guide appropriate treatment and support healthy growth while preventing long-term complications.", "We provide comprehensive evaluation and management of a wide range of paediatric orthopaedic conditions, with every child receiving an individualised assessment tailored to their age, stage of development and specific condition."]'::jsonb,
  'Our Paediatric Orthopaedic Services Include', '[{"title": "Limb Deformities", "desc": "Assessment and management of congenital and developmental limb deformities affecting the arms or legs, with treatment plans designed to support healthy growth and function."}, {"title": "Walking Abnormalities", "desc": "Evaluation of gait abnormalities, limping, in-toeing, out-toeing and other walking concerns to determine the underlying cause and recommend appropriate management."}, {"title": "Developmental Bone Conditions", "desc": "Diagnosis and treatment of developmental bone and joint disorders, ensuring early intervention where necessary to promote normal growth and mobility."}, {"title": "Paediatric Fractures", "desc": "Comprehensive care for fractures in children, with treatment focused on proper bone healing while protecting future growth and development."}]'::jsonb, 'Supporting Healthy Growth & Development', 'Our goal is to provide timely diagnosis, compassionate care and personalised treatment that supports every child''s healthy musculoskeletal development, working closely with parents and caregivers throughout.',
  false, 10)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('bone-tumours', '🩻', 'Bone Tumours', 'Careful evaluation and coordinated care for suspected bone tumours.', '["Bone tumours and bone lesions require careful evaluation to determine their nature and the most appropriate course of treatment. While many bone lesions are benign, some require further investigation to establish an accurate diagnosis and ensure timely management.", "We provide comprehensive assessment for patients with suspected bone tumours, using a structured approach that combines clinical evaluation, imaging review and coordinated investigations, with treatment recommendations based on each patient''s individual condition."]'::jsonb,
  'Our Bone Tumour Services Include', '[{"title": "Clinical Evaluation", "desc": "A thorough medical history and physical examination are performed to assess symptoms, identify potential risk factors and determine the most appropriate diagnostic pathway."}, {"title": "Imaging Review", "desc": "Detailed review of X-rays, CT scans, MRI scans and other relevant imaging studies to evaluate bone abnormalities and guide further assessment."}, {"title": "Initial Management", "desc": "Individualised treatment planning and early management to address symptoms, protect bone integrity and determine whether additional investigations or intervention are required."}, {"title": "Coordination of Further Investigations", "desc": "Arrangement and coordination of additional diagnostic tests, including advanced imaging and biopsy where appropriate, to establish a definitive diagnosis and guide ongoing care."}]'::jsonb, 'Early Diagnosis. Expert Guidance. Personalised Care.', 'Patients requiring specialised bone tumour surgery or advanced orthopaedic oncology care will be referred to recognised orthopaedic oncology specialists, ensuring comprehensive treatment and reassurance throughout every stage of the journey.',
  false, 11)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;
insert into cms_services (slug, icon, title, short, intro, includes_title, includes, closing_title, closing_text, show_on_home, sort_order)
values ('collaborative-specialist-care', '🤝', 'Collaborative Specialist Care', 'Coordinated referral to trusted subspecialists for complex conditions.', '["Some orthopaedic conditions require highly specialised expertise and multidisciplinary management to achieve the best possible outcomes. We believe every patient deserves access to the most appropriate level of care, particularly when advanced surgical intervention is required.", "When complex conditions extend beyond the scope of general orthopaedic practice, we work closely with experienced, peer-recognised orthopaedic subspecialists to ensure patients receive seamless care and ongoing support throughout every stage of their recovery."]'::jsonb,
  'Our Collaborative Care Approach', '[{"title": "Advanced Spinal Disorders", "desc": "Patients with complex spinal conditions requiring specialised spinal surgery will be referred to experienced spine surgeons with advanced expertise in cervical, thoracic and lumbar spinal disorders."}, {"title": "Paediatric Orthopaedic Conditions", "desc": "Children with complex congenital, developmental or surgical orthopaedic conditions are referred to dedicated paediatric orthopaedic specialists for age-appropriate treatment."}, {"title": "Bone Tumours & Orthopaedic Oncology", "desc": "Patients requiring specialised bone tumour surgery or advanced orthopaedic oncology management will be referred to recognised orthopaedic oncology specialists."}, {"title": "Coordinated Patient Care", "desc": "We work closely with trusted specialists and healthcare professionals to coordinate investigations, referrals, treatment planning and postoperative follow-up."}]'::jsonb, 'Working Together for the Best Possible Outcomes', 'By working in partnership with experienced subspecialty orthopaedic surgeons and multidisciplinary healthcare teams, we ensure every patient receives personalised, coordinated and evidence-based care that supports the best possible recovery.',
  false, 12)
on conflict (slug) do update set
  icon=excluded.icon, title=excluded.title, short=excluded.short, intro=excluded.intro,
  includes_title=excluded.includes_title, includes=excluded.includes,
  closing_title=excluded.closing_title, closing_text=excluded.closing_text,
  show_on_home=excluded.show_on_home, sort_order=excluded.sort_order;

-- Gallery cases (photo gallery, grouped by case)
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('knee-replacement', 'Total Knee Replacement', 'Pre- and post-operative imaging showing implant positioning and alignment.', '["/images/gallery/knee-replacement-1.jpg", "/images/gallery/knee-replacement-2.jpg", "/images/gallery/knee-replacement-3.jpg", "/images/gallery/knee-replacement-4.jpg"]'::jsonb, 0)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('hip-replacement', 'Total Hip Replacement', 'Case series showing restored hip joint anatomy after total replacement.', '["/images/gallery/hip-replacement-1.jpg", "/images/gallery/hip-replacement-2.jpg", "/images/gallery/hip-replacement-3.jpg", "/images/gallery/hip-replacement-4.jpg"]'::jsonb, 1)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('medial-osteoarthritis', 'Severe Medial Compartment Osteoarthritis', 'Progressive joint space narrowing and degenerative change in the medial knee compartment.', '["/images/gallery/medial-osteoarthritis-1.jpg", "/images/gallery/medial-osteoarthritis-2.jpg", "/images/gallery/medial-osteoarthritis-3.jpg", "/images/gallery/medial-osteoarthritis-4.jpg", "/images/gallery/medial-osteoarthritis-5.jpg"]'::jsonb, 2)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('quadriceps-rupture', 'Neglected Quadriceps Tendon Rupture', 'Surgical repair of a delayed-presentation quadriceps tendon injury.', '["/images/gallery/quadriceps-rupture-1.jpg", "/images/gallery/quadriceps-rupture-2.jpg", "/images/gallery/quadriceps-rupture-3.jpg", "/images/gallery/quadriceps-rupture-4.jpg", "/images/gallery/quadriceps-rupture-5.jpg", "/images/gallery/quadriceps-rupture-6.jpg"]'::jsonb, 3)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('erl-rupture', 'Spontaneous ERL Rupture in a 24-Year-Old', 'Tendon rupture repair in a young patient, from diagnosis through surgical correction.', '["/images/gallery/erl-rupture-1.jpg", "/images/gallery/erl-rupture-2.jpg", "/images/gallery/erl-rupture-3.jpg", "/images/gallery/erl-rupture-4.jpg", "/images/gallery/erl-rupture-5.jpg", "/images/gallery/erl-rupture-6.jpg"]'::jsonb, 4)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('tibia-stress-fracture', 'Stress Fracture of the Tibia', 'Imaging and management of an overuse stress fracture of the tibia.', '["/images/gallery/tibia-stress-fracture-1.jpg", "/images/gallery/tibia-stress-fracture-2.jpg", "/images/gallery/tibia-stress-fracture-3.jpg"]'::jsonb, 5)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('mcl-tear', 'MCL Substance Tear', 'Medial collateral ligament injury assessment.', '["/images/gallery/mcl-tear-1.jpg"]'::jsonb, 6)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('ulnar-nerve-decompression', 'Ulnar Nerve Decompression', 'Surgical decompression of the ulnar nerve at Guyon''s tunnel.', '["/images/gallery/ulnar-nerve-decompression-1.jpg", "/images/gallery/ulnar-nerve-decompression-2.jpg"]'::jsonb, 7)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;
insert into cms_gallery_cases (slug, title, description, images, sort_order)
values ('giant-cell-tumour', 'Giant Cell Tumour of Tendon Sheath', 'Excision of a benign soft-tissue tumour of the tendon sheath.', '["/images/gallery/giant-cell-tumour-1.jpg"]'::jsonb, 8)
on conflict (slug) do update set
  title=excluded.title, description=excluded.description, images=excluded.images, sort_order=excluded.sort_order;

-- Contact info
insert into cms_contact (id, address_lines, whatsapp_display, whatsapp_href, phone_display, phone_href, email, facebook, instagram, hours)
values (1, '["Suite 02-06, Level 6", "Riverson@Sembulan, Block A-1", "Lorong Riverson@Sembulan, Off Coastal Highway", "88100 Kota Kinabalu, Sabah"]'::jsonb, '+60 11-3666 1140', 'https://wa.me/601136661140',
  '+60 88-518 879', 'tel:+6088518879', 'enquiry@dharmaortho.my',
  'https://facebook.com/dharmaortho', 'https://instagram.com/orthodm', '[{"label": "Monday \u2013 Friday", "value": "9:00 AM \u2013 5:00 PM"}, {"label": "Saturday", "value": "9:00 AM \u2013 1:00 PM"}]'::jsonb)
on conflict (id) do update set
  address_lines=excluded.address_lines, whatsapp_display=excluded.whatsapp_display, whatsapp_href=excluded.whatsapp_href,
  phone_display=excluded.phone_display, phone_href=excluded.phone_href, email=excluded.email,
  facebook=excluded.facebook, instagram=excluded.instagram, hours=excluded.hours;
