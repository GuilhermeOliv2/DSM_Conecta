import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:dsm_conecta/main.dart';

void main() {
  testWidgets('requires explicit consent before enabling sensors', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const DsmConectaApp());

    await tester.scrollUntilVisible(
      find.text('Consentimento não concedido. Nenhum sensor será iniciado.'),
      200,
      scrollable: find.byType(Scrollable),
    );
    expect(
      find.text('Consentimento não concedido. Nenhum sensor será iniciado.'),
      findsOneWidget,
    );
    expect(
      find.text(
        'Consentimento concedido. A integração dos sensores poderá ser iniciada.',
      ),
      findsNothing,
    );

    await tester.tap(
      find.text('Li e compreendi quais dados poderão ser coletados.'),
    );
    await tester.pump();
    await tester.tap(
      find.widgetWithText(FilledButton, 'Autorizar uso dos sensores'),
    );
    await tester.pump();

    expect(
      find.text(
        'Consentimento concedido. A integração dos sensores poderá ser iniciada.',
      ),
      findsOneWidget,
    );

    await tester.scrollUntilVisible(
      find.widgetWithText(OutlinedButton, 'Revogar consentimento'),
      200,
      scrollable: find.byType(Scrollable),
    );
    await tester.tap(
      find.widgetWithText(OutlinedButton, 'Revogar consentimento'),
    );
    await tester.pump();

    await tester.scrollUntilVisible(
      find.text('Consentimento não concedido. Nenhum sensor será iniciado.'),
      200,
      scrollable: find.byType(Scrollable),
    );
    expect(
      find.text('Consentimento não concedido. Nenhum sensor será iniciado.'),
      findsOneWidget,
    );
  });
}
